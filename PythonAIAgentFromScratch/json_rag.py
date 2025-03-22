import json
import os
from typing import List, Dict, Any
from dotenv import load_dotenv
import openai
import yfinance as yf
import requests
from bs4 import BeautifulSoup
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
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
        self.embeddings = OpenAIEmbeddings()
        
        # Initialize OpenAI
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        
        # Load and process JSON data
        self._load_and_process_data()
    
    def _load_and_process_data(self):
        """Load JSON data and create vector store."""
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert JSON data to text documents
            documents = []
            for item in data:
                # Convert each item to a string representation
                text = json.dumps(item, ensure_ascii=False)
                documents.append(Document(
                    page_content=text,
                    metadata={"source": self.json_file_path}
                ))
            
            # Split documents into chunks
            texts = self.text_splitter.split_documents(documents)
            
            # Create vector store
            self.vector_store = FAISS.from_documents(texts, self.embeddings)
            
        except FileNotFoundError:
            print(f"Warning: {self.json_file_path} not found. Please add data to the file.")
            self.vector_store = None
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {self.json_file_path}")
            self.vector_store = None
    
    def _fetch_yahoo_finance_data(self, symbol: str) -> str:
        """Fetch data from Yahoo Finance."""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract relevant information
            data = {
                "symbol": symbol,
                "name": info.get('longName', ''),
                "sector": info.get('sector', ''),
                "description": info.get('longBusinessSummary', ''),
                "key_metrics": {
                    "market_cap": info.get('marketCap', 0),
                    "pe_ratio": info.get('forwardPE', 0),
                    "dividend_yield": info.get('dividendYield', 0)
                }
            }
            return json.dumps(data)
        except Exception as e:
            print(f"Error fetching Yahoo Finance data: {str(e)}")
            return ""
    
    def _fetch_investopedia_data(self, query: str) -> str:
        """Fetch data from Investopedia."""
        try:
            # Note: This is a simplified example. In a real implementation,
            # you would need to use Investopedia's API or proper web scraping
            url = f"https://www.investopedia.com/search?q={query}"
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant information (this is a simplified example)
            articles = []
            for article in soup.find_all('article', limit=3):
                title = article.find('h2').text if article.find('h2') else ''
                summary = article.find('p').text if article.find('p') else ''
                articles.append({
                    "title": title,
                    "summary": summary
                })
            
            return json.dumps({"articles": articles})
        except Exception as e:
            print(f"Error fetching Investopedia data: {str(e)}")
            return ""
    
    def query(self, query: str, k: int = 3) -> str:
        """Query the RAG system and generate a response."""
        if not self.vector_store:
            return "Error: No data available. Please ensure finance.json contains valid data."
        
        # Retrieve relevant documents from vector store
        docs = self.vector_store.similarity_search(query, k=k)
        
        # Prepare context from retrieved documents
        context = "\n".join([doc.page_content for doc in docs])
        
        # If OpenAI API key is not available, use alternative sources
        if not self.openai_api_key:
            # Extract potential symbols from the query
            words = query.split()
            symbols = [word for word in words if word.isupper() and len(word) <= 5]
            
            # Fetch additional data from Yahoo Finance and Investopedia
            additional_context = []
            for symbol in symbols:
                yahoo_data = self._fetch_yahoo_finance_data(symbol)
                if yahoo_data:
                    additional_context.append(yahoo_data)
            
            investopedia_data = self._fetch_investopedia_data(query)
            if investopedia_data:
                additional_context.append(investopedia_data)
            
            # Combine all context
            context = context + "\n" + "\n".join(additional_context)
            
            # Use a simple template for response
            return f"""
            Based on the available data:
            
            {context}
            
            Summary:
            The above information has been gathered from multiple sources including our knowledge base, 
            Yahoo Finance, and Investopedia. Please note that this is a simplified analysis and should 
            not be considered as financial advice.
            """
        
        # If OpenAI API key is available, use GPT-4
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a financial advisor. Provide clear, concise, and accurate information based on the given context."},
                    {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}\n\nPlease provide a detailed answer based on the context."}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def update_data(self):
        """Reload and process the JSON data."""
        self._load_and_process_data() 