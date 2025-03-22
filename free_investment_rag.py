from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from typing import List, Dict, Any
import json
import requests
from bs4 import BeautifulSoup
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

class FreeInvestmentRAG:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        self.vector_store = None
        self.sources = {
            'yahoo_finance': self._fetch_yahoo_finance_data,
            'marketwatch': self._fetch_marketwatch_data,
            'investopedia': self._fetch_investopedia_data
        }
        
    def _fetch_yahoo_finance_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch data from Yahoo Finance"""
        try:
            stock = yf.Ticker(symbol)
            info = stock.info
            return {
                'source': 'Yahoo Finance',
                'symbol': symbol,
                'company_name': info.get('longName'),
                'current_price': info.get('currentPrice'),
                'market_cap': info.get('marketCap'),
                'pe_ratio': info.get('forwardPE'),
                'dividend_yield': info.get('dividendYield'),
                'sector': info.get('sector'),
                'industry': info.get('industry')
            }
        except Exception as e:
            return {'error': f'Error fetching Yahoo Finance data: {str(e)}'}

    def _fetch_marketwatch_data(self, symbol: str) -> Dict[str, Any]:
        """Fetch data from MarketWatch"""
        try:
            url = f'https://www.marketwatch.com/investing/stock/{symbol}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant data (this is a simplified example)
            return {
                'source': 'MarketWatch',
                'symbol': symbol,
                'price': soup.find('span', {'class': 'price'}).text if soup.find('span', {'class': 'price'}) else None,
                'change': soup.find('span', {'class': 'change'}).text if soup.find('span', {'class': 'change'}) else None
            }
        except Exception as e:
            return {'error': f'Error fetching MarketWatch data: {str(e)}'}

    def _fetch_investopedia_data(self, term: str) -> Dict[str, Any]:
        """Fetch educational content from Investopedia"""
        try:
            url = f'https://www.investopedia.com/search?q={term}'
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract relevant content (this is a simplified example)
            return {
                'source': 'Investopedia',
                'term': term,
                'content': soup.find('div', {'class': 'search-results'}).text if soup.find('div', {'class': 'search-results'}) else None
            }
        except Exception as e:
            return {'error': f'Error fetching Investopedia data: {str(e)}'}

    def add_investment_data(self, symbol: str, term: str = None) -> str:
        """Add investment data from multiple sources"""
        data = []
        
        # Fetch data from Yahoo Finance
        yahoo_data = self._fetch_yahoo_finance_data(symbol)
        if 'error' not in yahoo_data:
            data.append(yahoo_data)
            
        # Fetch data from MarketWatch
        marketwatch_data = self._fetch_marketwatch_data(symbol)
        if 'error' not in marketwatch_data:
            data.append(marketwatch_data)
            
        # Fetch educational content from Investopedia if term is provided
        if term:
            investopedia_data = self._fetch_investopedia_data(term)
            if 'error' not in investopedia_data:
                data.append(investopedia_data)
        
        # Convert data to text and create documents
        texts = [json.dumps(item, indent=2) for item in data]
        docs = self.text_splitter.create_documents(texts)
        
        # Add to vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(docs, self.text_splitter)
        else:
            self.vector_store.add_documents(docs)
        
        return f"Added {len(docs)} documents to the RAG system"

    def query_investment_knowledge(self, query: str) -> str:
        """Query the investment knowledge base"""
        if self.vector_store is None:
            return "No investment data available. Please add data first."
            
        # Search for relevant documents
        docs = self.vector_store.similarity_search(query, k=3)
        
        # Format the response
        response = "Here's what I found:\n\n"
        for i, doc in enumerate(docs, 1):
            response += f"Source {i}:\n{doc.page_content}\n\n"
            
        return response

    def get_investment_recommendation(self, amount: float, risk_tolerance: str = 'moderate') -> str:
        """Generate investment recommendations based on amount and risk tolerance"""
        if self.vector_store is None:
            return "Please add investment data first to get recommendations."
            
        # Create a query based on the amount and risk tolerance
        query = f"investment strategy for {amount} dollars with {risk_tolerance} risk tolerance"
        docs = self.vector_store.similarity_search(query, k=3)
        
        # Format the recommendation
        recommendation = f"Based on your investment amount of ${amount:,.2f} and {risk_tolerance} risk tolerance:\n\n"
        for doc in docs:
            recommendation += f"- {doc.page_content}\n"
            
        return recommendation 