from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from typing import List, Dict, Any, Optional
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
from rag_tools import InvestmentRAG as OpenAIRAG
from tools import search_tool, wiki_tool
import openai
from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class UserInvestmentProfile(BaseModel):
    """Structured user investment profile"""
    user_id: str = Field(..., description="Unique identifier for the user")
    investment_goals: List[str] = Field(..., description="List of investment goals (e.g., growth, income, preservation)")
    risk_tolerance: str = Field(..., description="Risk tolerance level (conservative, moderate, aggressive)")
    investment_horizon: str = Field(..., description="Investment time horizon (short-term, medium-term, long-term)")
    preferred_sectors: List[str] = Field(default_factory=list, description="Preferred investment sectors")
    excluded_sectors: List[str] = Field(default_factory=list, description="Sectors to avoid")
    monthly_investment: float = Field(..., description="Monthly investment amount")
    total_investable_assets: float = Field(..., description="Total investable assets")
    current_portfolio: Optional[Dict[str, Any]] = Field(None, description="Current portfolio holdings")
    investment_constraints: List[str] = Field(default_factory=list, description="Any investment constraints or preferences")
    tax_considerations: Optional[Dict[str, Any]] = Field(None, description="Tax-related considerations")
    rebalancing_frequency: str = Field(default="quarterly", description="Preferred portfolio rebalancing frequency")

class InvestmentHistory(BaseModel):
    """Track user's investment history"""
    timestamp: datetime = Field(default_factory=datetime.now)
    action: str = Field(..., description="Investment action taken")
    amount: float = Field(..., description="Amount involved in the action")
    investment_type: str = Field(..., description="Type of investment")
    details: Dict[str, Any] = Field(..., description="Additional details about the action")

class InvestmentTransitionKnowledge:
    """Knowledge base for transitioning from stock user to strategic investor"""
    
    MINDSET_SHIFTS = {
        "short_term_to_long_term": {
            "before": "Focusing on daily price movements and quick profits",
            "after": "Building long-term wealth through compound interest",
            "example": "Amazon stock dropped 90% in 2000 but grew 100x by 2020"
        },
        "emotional_to_analytical": {
            "before": "Making decisions based on market sentiment",
            "after": "Using data-driven analysis and fundamental research",
            "example": "Buffett's famous quote: 'Be fearful when others are greedy'"
        },
        "speculative_to_strategic": {
            "before": "Chasing hot tips and trends",
            "after": "Following a well-defined investment strategy",
            "example": "Peter Lynch's 'Invest in what you know' principle"
        }
    }
    
    STRATEGY_FRAMEWORKS = {
        "value_investing": {
            "description": "Buy undervalued companies with strong fundamentals",
            "metrics": ["P/E ratio", "Price to Book", "ROE", "Debt/Equity"],
            "example": "Warren Buffett's investment in Coca-Cola in 1988"
        },
        "growth_investing": {
            "description": "Focus on companies with high revenue/profit growth",
            "metrics": ["Revenue Growth", "Profit Margins", "Market Share"],
            "example": "Peter Lynch's investment in Starbucks in 1992"
        },
        "dividend_investing": {
            "description": "Target companies with consistent dividend payments",
            "metrics": ["Dividend Yield", "Payout Ratio", "Dividend Growth"],
            "example": "Johnson & Johnson's 60+ years of dividend increases"
        }
    }
    
    RISK_MANAGEMENT_RULES = {
        "position_sizing": {
            "rule": "Never invest more than 5% in a single stock",
            "rationale": "Protects against individual stock risk",
            "example": "If portfolio is $100,000, max $5,000 per stock"
        },
        "stop_loss": {
            "rule": "Set stop-loss at 15% below purchase price",
            "rationale": "Limits downside while allowing for normal volatility",
            "example": "Buy at $100, stop-loss at $85"
        },
        "cash_reserve": {
            "rule": "Maintain 20% cash for market opportunities",
            "rationale": "Allows buying quality stocks during market crashes",
            "example": "During March 2020 crash, many quality stocks were available at discounts"
        }
    }
    
    PORTFOLIO_METRICS = {
        "valuation": {
            "P/E_ratio": {
                "ideal": "Below industry average",
                "example": "TCS P/E 30 vs Infosys 25",
                "interpretation": "Lower P/E might indicate better value"
            },
            "ROE": {
                "ideal": "Above 15%",
                "example": "Asian Paints ROE 25%",
                "interpretation": "Higher ROE indicates efficient capital usage"
            },
            "Debt_to_Equity": {
                "ideal": "Below 1",
                "example": "Reliance 0.8",
                "interpretation": "Lower ratio indicates less financial risk"
            }
        }
    }

class IntegratedInvestmentRAG:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        self.vector_store = None
        self.openai_rag = OpenAIRAG() if OpenAIRAG else None
        self.transition_knowledge = InvestmentTransitionKnowledge()
        self.sources = {
            'yahoo_finance': self._fetch_yahoo_finance_data,
            'marketwatch': self._fetch_marketwatch_data,
            'investopedia': self._fetch_investopedia_data,
            'web_search': self._web_search,
            'wikipedia': self._wiki_search
        }
        self.user_profiles: Dict[str, UserInvestmentProfile] = {}
        self.investment_history: Dict[str, List[InvestmentHistory]] = {}
        self.user_data = {}
        
    def _fetch_yahoo_finance_data(self, symbol: str) -> str:
        """Fetch data from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return f"""
            Company: {info.get('longName', 'N/A')}
            Sector: {info.get('sector', 'N/A')}
            Industry: {info.get('industry', 'N/A')}
            Market Cap: ${info.get('marketCap', 0):,.2f}
            P/E Ratio: {info.get('forwardPE', 'N/A')}
            Dividend Yield: {info.get('dividendYield', 'N/A')}%
            """
        except Exception as e:
            return f"Error fetching data for {symbol}: {str(e)}"

    def _fetch_marketwatch_data(self, symbol: str) -> str:
        """Fetch data from MarketWatch"""
        try:
            url = f"https://www.marketwatch.com/investing/stock/{symbol}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return f"MarketWatch data for {symbol}"
        except Exception as e:
            return f"Error fetching MarketWatch data for {symbol}: {str(e)}"

    def _fetch_investopedia_data(self, query: str) -> str:
        """Fetch educational content from Investopedia"""
        try:
            url = f"https://www.investopedia.com/search?q={query}"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return f"Investopedia content for {query}"
        except Exception as e:
            return f"Error fetching Investopedia data: {str(e)}"

    def _web_search(self, query: str) -> str:
        """Perform web search for investment information"""
        try:
            # Implement web search functionality
            return f"Web search results for {query}"
        except Exception as e:
            return f"Error performing web search: {str(e)}"

    def _wiki_search(self, query: str) -> str:
        """Search Wikipedia for investment-related information"""
        try:
            # Implement Wikipedia search functionality
            return f"Wikipedia content for {query}"
        except Exception as e:
            return f"Error searching Wikipedia: {str(e)}"

    def add_investment_data(self, symbol: str, use_openai: bool = False) -> str:
        """Add investment data from various sources"""
        try:
            # Fetch data from different sources
            yahoo_data = self._fetch_yahoo_finance_data(symbol)
            marketwatch_data = self._fetch_marketwatch_data(symbol)
            investopedia_data = self._fetch_investopedia_data(symbol)
            web_data = self._web_search(symbol)
            wiki_data = self._wiki_search(symbol)
            
            # Combine all data
            combined_data = f"""
            Investment Data for {symbol}:
            
            Yahoo Finance:
            {yahoo_data}
            
            MarketWatch:
            {marketwatch_data}
            
            Investopedia:
            {investopedia_data}
            
            Web Search:
            {web_data}
            
            Wikipedia:
            {wiki_data}
            """
            
            # Create documents and add to vector store
            documents = self.text_splitter.create_documents([combined_data])
            
            if use_openai and os.getenv('OPENAI_API_KEY'):
                embeddings = OpenAIEmbeddings()
                if self.vector_store is None:
                    self.vector_store = FAISS.from_documents(documents, embeddings)
                else:
                    self.vector_store.add_documents(documents)
            
            return f"Successfully added investment data for {symbol}"
        except Exception as e:
            return f"Error adding investment data: {str(e)}"

    def add_user_investment_data(self, profile_data: Dict[str, Any]) -> str:
        """Add or update user's investment profile"""
        try:
            user_id = profile_data.get('user_id')
            if not user_id:
                return "Error: user_id is required"
            
            self.user_data[user_id] = profile_data
            self.user_profiles[user_id] = UserInvestmentProfile(**profile_data)
            self.investment_history[user_id] = []
            return f"Successfully added/updated profile for user {user_id}"
        except Exception as e:
            return f"Error adding user data: {str(e)}"

    def add_investment_history(self, user_id: str, history_data: Dict[str, Any]) -> str:
        """Add investment history entry for a user"""
        try:
            if user_id not in self.user_data:
                return f"Error: User {user_id} not found"
            
            if 'investment_history' not in self.user_data[user_id]:
                self.user_data[user_id]['investment_history'] = []
            
            self.user_data[user_id]['investment_history'].append(history_data)
            self.investment_history[user_id].append(InvestmentHistory(**history_data))
            return f"Successfully added history entry for user {user_id}"
        except Exception as e:
            return f"Error adding investment history: {str(e)}"

    def _generate_gpt4_recommendation(self, context: str, risk_tolerance: str) -> str:
        """Generate investment recommendation using GPT-4"""
        try:
            if not os.getenv('OPENAI_API_KEY'):
                return "OpenAI API key not configured"
            
            client = ChatOpenAI(model="gpt-4")
            
            prompt = f"""
            As an expert investment advisor, analyze the following context and provide a detailed investment recommendation.
            Consider the user's risk tolerance: {risk_tolerance}
            
            Context:
            {context}
            
            Provide a structured recommendation including:
            1. Portfolio Allocation
            2. Investment Rationale
            3. Implementation Strategy
            4. Risk Management
            5. Future Considerations
            
            Focus on transitioning from a stock user to a strategic investor mindset.
            """
            
            response = client.invoke(prompt)
            return response.content
        except Exception as e:
            return f"Error generating recommendation: {str(e)}"

    def get_investment_recommendation(self, amount: float, risk_tolerance: str = 'moderate', user_id: Optional[str] = None, use_openai: bool = False) -> str:
        """Get investment recommendations"""
        try:
            # Prepare context from user data if available
            user_context = ""
            if user_id and user_id in self.user_data:
                user_profile = self.user_data[user_id]
                user_context = f"""
                User Profile:
                - Investment Goals: {', '.join(user_profile.get('investment_goals', []))}
                - Risk Tolerance: {user_profile.get('risk_tolerance', 'moderate')}
                - Preferred Sectors: {', '.join(user_profile.get('preferred_sectors', []))}
                - Current Portfolio: {json.dumps(user_profile.get('current_portfolio', {}), indent=2)}
                """
            
            # Get relevant documents from vector store
            relevant_docs = []
            if self.vector_store:
                query = f"investment recommendation for {risk_tolerance} risk tolerance"
                relevant_docs = self.vector_store.similarity_search(query, k=3)
            
            # Combine context
            context = f"""
            Investment Amount: ${amount:,.2f}
            Risk Tolerance: {risk_tolerance}
            
            {user_context}
            
            Relevant Information:
            {[doc.page_content for doc in relevant_docs]}
            
            Transition Knowledge:
            Mindset Shifts:
            {json.dumps(self.transition_knowledge.MINDSET_SHIFTS, indent=2)}
            
            Strategy Frameworks:
            {json.dumps(self.transition_knowledge.STRATEGY_FRAMEWORKS, indent=2)}
            
            Risk Management Rules:
            {json.dumps(self.transition_knowledge.RISK_MANAGEMENT_RULES, indent=2)}
            
            Portfolio Metrics:
            {json.dumps(self.transition_knowledge.PORTFOLIO_METRICS, indent=2)}
            """
            
            if use_openai and os.getenv('OPENAI_API_KEY'):
                return self._generate_gpt4_recommendation(context, risk_tolerance)
            else:
                return f"""
                Basic Investment Recommendation:
                
                Based on your risk tolerance ({risk_tolerance}) and investment amount (${amount:,.2f}):
                
                1. Portfolio Allocation:
                - 60% Large Cap Stocks
                - 20% Mid Cap Stocks
                - 10% Bonds
                - 10% Cash
                
                2. Investment Strategy:
                - Focus on companies with strong fundamentals
                - Maintain a long-term perspective
                - Regular portfolio rebalancing
                
                3. Risk Management:
                - Diversify across sectors
                - Set stop-loss orders
                - Keep emergency fund separate
                
                4. Next Steps:
                - Review your investment goals
                - Create a detailed investment plan
                - Start with index funds
                - Gradually add individual stocks
                """

    def query_investment_knowledge(self, query: str, use_openai: bool = False) -> str:
        """Query investment knowledge"""
        try:
            # Get relevant documents from vector store
            relevant_docs = []
            if self.vector_store:
                relevant_docs = self.vector_store.similarity_search(query, k=3)
            
            # Combine context
            context = f"""
            Query: {query}
            
            Relevant Information:
            {[doc.page_content for doc in relevant_docs]}
            
            Transition Knowledge:
            {json.dumps(self.transition_knowledge.__dict__, indent=2)}
            """
            
            if use_openai and os.getenv('OPENAI_API_KEY'):
                client = ChatOpenAI(model="gpt-4")
                prompt = f"""
                As an expert investment advisor, answer the following question:
                {query}
                
                Use this context to provide a detailed answer:
                {context}
                
                Focus on helping users transition from stock trading to strategic investing.
                """
                
                response = client.invoke(prompt)
                return response.content
            else:
                return f"Basic answer for: {query}\nPlease configure OpenAI API key for detailed analysis."
        except Exception as e:
            return f"Error querying investment knowledge: {str(e)}" 