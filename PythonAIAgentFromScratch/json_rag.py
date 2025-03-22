import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
from openai import OpenAI
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

# Load environment variables
load_dotenv()

class JSONRAG:
    def __init__(self, json_file_path: str = "finance.json"):
        """Initialize the RAG system with JSON data."""
        self.json_file_path = json_file_path
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.vector_store = None
        
        # Initialize OpenAI
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            print("Warning: OPENAI_API_KEY not found. Some features will be limited.")
            self.embeddings = None
            self.client = None
        else:
            self.embeddings = OpenAIEmbeddings()
            self.client = OpenAI(api_key=self.openai_api_key)
        
        # Load and process JSON data
        self._load_and_process_data()
    
    def _load_and_process_data(self):
        """Load JSON data and create vector store."""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                self.data = json.load(f)
            
            # Convert JSON data to text documents
            documents = []
            for item in self.data:
                # Convert each item to a string representation
                text = json.dumps(item, ensure_ascii=False)
                documents.append(Document(
                    page_content=text,
                    metadata={"source": self.json_file_path}
                ))
            
            # Split documents into chunks
            texts = self.text_splitter.split_documents(documents)
            
            # Create vector store only if embeddings are available
            if self.embeddings:
                self.vector_store = FAISS.from_documents(texts, self.embeddings)
            else:
                print("Warning: Vector store not created due to missing API key")
                self.vector_store = None
            
        except FileNotFoundError:
            print(f"Warning: {self.json_file_path} not found. Please add data to the file.")
            self.vector_store = None
            self.data = []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.json_file_path}")
            self.vector_store = None
            self.data = []

    def _fetch_yahoo_finance_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch financial data from Yahoo Finance."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract relevant financial information
            financial_data = {
                "symbol": symbol,
                "company_name": info.get('longName', ''),
                "sector": info.get('sector', ''),
                "industry": info.get('industry', ''),
                "market_cap": info.get('marketCap', 0),
                "pe_ratio": info.get('forwardPE', 0),
                "dividend_yield": info.get('dividendYield', 0),
                "52_week_high": info.get('fiftyTwoWeekHigh', 0),
                "52_week_low": info.get('fiftyTwoWeekLow', 0),
                "volume": info.get('volume', 0),
                "avg_volume": info.get('averageVolume', 0),
                "financial_metrics": {
                    "revenue": info.get('totalRevenue', 0),
                    "profit_margin": info.get('profitMargins', 0),
                    "operating_margin": info.get('operatingMargins', 0),
                    "return_on_equity": info.get('returnOnEquity', 0),
                    "total_debt": info.get('totalDebt', 0),
                    "total_cash": info.get('totalCash', 0)
                }
            }
            return financial_data
        except Exception as e:
            print(f"Error fetching Yahoo Finance data for {symbol}: {str(e)}")
            return {}

    def _fetch_investopedia_data(self, term: str) -> Dict[str, Any]:
        """Fetch financial education data from Investopedia."""
        try:
            # Format search term for URL
            search_term = term.replace(' ', '+')
            url = f"https://www.investopedia.com/search?q={search_term}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract financial education content
            education_data = {
                "term": term,
                "articles": [],
                "definitions": [],
                "related_terms": []
            }
            
            # Get article summaries
            articles = soup.find_all('div', class_='search-article')
            for article in articles[:3]:  # Limit to top 3 articles
                title = article.find('h3')
                summary = article.find('p')
                if title and summary:
                    education_data["articles"].append({
                        "title": title.text.strip(),
                        "summary": summary.text.strip()
                    })
            
            return education_data
        except Exception as e:
            print(f"Error fetching Investopedia data for {term}: {str(e)}")
            return {}
    
    def query(self, query: str, k: int = 3) -> str:
        """Query the RAG system and generate a response."""
        if not self.vector_store or not self.data:
            return "Error: No financial data available. Please ensure the JSON file contains valid financial information."
        
        # Check if query is finance-related
        finance_keywords = self._extract_finance_keywords(query)
        if not finance_keywords:
            return "I can only answer questions related to financial topics and investment data available in our database."
        
        # Retrieve relevant documents from vector store
        docs = self.vector_store.similarity_search(query, k=k)
        
        # Prepare context from retrieved documents
        context = "\n".join([doc.page_content for doc in docs])
        
        # Extract potential stock symbols and financial terms
        words = query.split()
        symbols = [word for word in words if word.isupper() and len(word) <= 5]
        
        # Fetch additional financial data
        financial_context = []
        
        # Get stock data for any symbols
        for symbol in symbols:
            stock_data = self._fetch_yahoo_finance_data(symbol)
            if stock_data:
                financial_context.append(f"Stock Data for {symbol}:")
                financial_context.append(json.dumps(stock_data, indent=2))
        
        # Get educational content for finance keywords
        for keyword in finance_keywords:
            edu_data = self._fetch_investopedia_data(keyword)
            if edu_data and edu_data.get("articles"):
                financial_context.append(f"Financial Education for {keyword}:")
                financial_context.append(json.dumps(edu_data, indent=2))
        
        # Combine all financial context
        full_context = context + "\n\n" + "\n\n".join(financial_context)
        
        # If OpenAI API key is not available, return raw financial data
        if not self.client:
            return f"""
            Based on the available financial data:
            
            {full_context}
            
            Note: This is raw financial data from our database and external sources.
            """
        
        # If OpenAI API key is available, use GPT-4 with strict financial focus
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {
                        "role": "system", 
                        "content": """You are a financial data analyzer. Your responses must be based EXCLUSIVELY on the financial data provided.
                        ONLY use the financial data and market information in the context.
                        DO NOT add any external knowledge or general advice.
                        If specific financial information is not in the context, say 'This financial data is not available in our database.'
                        Focus solely on analyzing and explaining the financial data provided."""
                    },
                    {
                        "role": "user", 
                        "content": f"Financial Data:\n{full_context}\n\nQuestion: {query}\n\nAnalyze this financial data and provide insights using ONLY the information provided."
                    }
                ],
                temperature=0.3  # Lower temperature for more focused financial analysis
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error analyzing financial data: {str(e)}"
    
    def _extract_finance_keywords(self, query: str) -> List[str]:
        """Extract finance-related keywords from query."""
        finance_terms = [
            "invest", "stock", "bond", "fund", "market", "portfolio", "risk",
            "return", "dividend", "asset", "equity", "trading", "financial",
            "money", "capital", "profit", "loss", "balance", "account", "price",
            "value", "growth", "income", "debt", "credit", "interest", "rate",
            "sector", "industry", "revenue", "margin", "cash", "volume", "yield",
            "market cap", "PE ratio", "ROE", "debt", "earnings", "volatility"
        ]
        return [term for term in finance_terms if term.lower() in query.lower()]
    
    def update_data(self):
        """Reload and process the JSON data."""
        self._load_and_process_data() 