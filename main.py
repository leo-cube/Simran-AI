from dotenv import load_dotenv
import os
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from enhanced_tools import (
    search_tool, 
    wiki_tool, 
    save_tool, 
    dynamic_rag_tool,
    rag_query_tool, 
    visualization_tool
)
from integrated_rag import IntegratedInvestmentRAG, UserInvestmentProfile, InvestmentHistory
import json
from datetime import datetime

load_dotenv()

# Initialize the Integrated Investment RAG system
investment_rag = IntegratedInvestmentRAG()

# Pre-existing user profiles
predefined_profiles = {
    "user1": {
        "user_id": "user1",
        "investment_goals": ["growth", "income"],
        "risk_tolerance": "moderate",
        "investment_horizon": "long-term",
        "preferred_sectors": ["technology", "healthcare", "renewable energy"],
        "monthly_investment": 1000,
        "total_investable_assets": 50000,
        "current_portfolio": {
            "stocks": {
                "AAPL": {"shares": 10, "avg_price": 150},
                "MSFT": {"shares": 15, "avg_price": 280},
                "GOOGL": {"shares": 5, "avg_price": 2500}
            },
            "etfs": {
                "VOO": {"shares": 20, "avg_price": 350},
                "QQQ": {"shares": 15, "avg_price": 380}
            }
        },
        "investment_constraints": ["no tobacco", "no weapons"],
        "tax_considerations": {"tax_bracket": "24%", "retirement_accounts": True},
        "rebalancing_frequency": "quarterly"
    },
    "user2": {
        "user_id": "user2",
        "investment_goals": ["preservation", "income"],
        "risk_tolerance": "conservative",
        "investment_horizon": "medium-term",
        "preferred_sectors": ["utilities", "consumer staples", "real estate"],
        "monthly_investment": 500,
        "total_investable_assets": 25000,
        "current_portfolio": {
            "stocks": {
                "JNJ": {"shares": 8, "avg_price": 160},
                "PG": {"shares": 12, "avg_price": 140}
            },
            "etfs": {
                "VTI": {"shares": 25, "avg_price": 220},
                "VNQ": {"shares": 20, "avg_price": 85}
            }
        },
        "investment_constraints": ["no fossil fuels"],
        "tax_considerations": {"tax_bracket": "22%", "retirement_accounts": True},
        "rebalancing_frequency": "semi-annual"
    }
}

# Pre-existing investment history
predefined_history = {
    "user1": [
        {
            "action": "buy",
            "amount": 5000,
            "investment_type": "stock",
            "details": {
                "symbol": "AAPL",
                "shares": 10,
                "price_per_share": 150
            }
        },
        {
            "action": "buy",
            "amount": 4200,
            "investment_type": "stock",
            "details": {
                "symbol": "MSFT",
                "shares": 15,
                "price_per_share": 280
            }
        }
    ],
    "user2": [
        {
            "action": "buy",
            "amount": 2400,
            "investment_type": "stock",
            "details": {
                "symbol": "JNJ",
                "shares": 8,
                "price_per_share": 160
            }
        }
    ]
}

def setup_predefined_data():
    """Set up predefined user profiles and investment history"""
    for user_id, profile_data in predefined_profiles.items():
        investment_rag.add_user_investment_data(profile_data)
        
    for user_id, history_list in predefined_history.items():
        for history_data in history_list:
            investment_rag.add_investment_history(user_id, history_data)

def get_investment_recommendation(amount: float, risk_tolerance: str = 'moderate', user_id: Optional[str] = None) -> str:
    """Get investment recommendations using the integrated RAG system"""
    # Add some popular investment options to the RAG system
    popular_symbols = ['VOO', 'AAPL', 'MSFT', 'GOOGL', 'AMZN']
    for symbol in popular_symbols:
        investment_rag.add_investment_data(symbol, use_openai=bool(os.getenv('OPENAI_API_KEY')))
    
    # Get the recommendation
    return investment_rag.get_investment_recommendation(amount, risk_tolerance, user_id, use_openai=bool(os.getenv('OPENAI_API_KEY')))

def query_investment_knowledge(query: str) -> str:
    """Query investment knowledge using the integrated RAG system"""
    return investment_rag.query_investment_knowledge(query, use_openai=bool(os.getenv('OPENAI_API_KEY')))

def analyze_new_investment(amount: float, risk_tolerance: str, user_id: str) -> str:
    """Analyze new investment opportunities"""
    print("\nAnalyzing new investment opportunities...")
    print(f"Amount: ${amount:,.2f}")
    print(f"Risk Tolerance: {risk_tolerance}")
    
    # Get market analysis
    market_query = "What are the current market trends and opportunities?"
    market_analysis = query_investment_knowledge(market_query)
    
    # Get sector analysis based on user preferences
    user_profile = predefined_profiles[user_id]
    sector_query = f"What are the best opportunities in {', '.join(user_profile['preferred_sectors'])} sectors?"
    sector_analysis = query_investment_knowledge(sector_query)
    
    # Get specific recommendations
    recommendation = get_investment_recommendation(amount, risk_tolerance, user_id)
    
    return f"""
Market Analysis:
{market_analysis}

Sector Analysis:
{sector_analysis}

Investment Recommendation:
{recommendation}
"""

def review_portfolio(user_id: str) -> str:
    """Review and optimize existing portfolio"""
    user_profile = predefined_profiles[user_id]
    portfolio = user_profile['current_portfolio']
    
    # Calculate portfolio value
    total_value = 0
    for asset_type, holdings in portfolio.items():
        for symbol, details in holdings.items():
            total_value += details['shares'] * details['avg_price']
    
    # Get portfolio analysis
    portfolio_query = "What are the best strategies for portfolio optimization?"
    portfolio_analysis = query_investment_knowledge(portfolio_query)
    
    # Get rebalancing recommendations
    rebalancing_query = f"Based on the current portfolio value of ${total_value:,.2f}, what rebalancing strategies would you recommend?"
    rebalancing_advice = query_investment_knowledge(rebalancing_query)
    
    return f"""
Portfolio Summary:
Total Value: ${total_value:,.2f}
Current Holdings:
{json.dumps(portfolio, indent=2)}

Portfolio Analysis:
{portfolio_analysis}

Rebalancing Recommendations:
{rebalancing_advice}
"""

if __name__ == "__main__":
    # Set up predefined data
    setup_predefined_data()
    
    print("""
Welcome to the Enhanced Investment Advisor!
-----------------------------------------
API Status:
- OpenAI API: {}
    """.format(
        "Available" if os.getenv('OPENAI_API_KEY') else "Not configured"
    ))
    
    print("\nAvailable Users:")
    print("1. User 1 - Growth & Income Focus")
    print("2. User 2 - Conservative Income Focus")
    user_choice = input("\nSelect user (1/2): ")
    
    user_id = "user1" if user_choice == "1" else "user2"
    user_profile = predefined_profiles[user_id]
    
    print(f"\nSelected User Profile:")
    print(f"Investment Goals: {', '.join(user_profile['investment_goals'])}")
    print(f"Risk Tolerance: {user_profile['risk_tolerance']}")
    print(f"Monthly Investment: ${user_profile['monthly_investment']:,.2f}")
    print(f"Total Assets: ${user_profile['total_investable_assets']:,.2f}")
    
    print("\nCurrent Portfolio:")
    for asset_type, holdings in user_profile['current_portfolio'].items():
        print(f"\n{asset_type.upper()}:")
        for symbol, details in holdings.items():
            print(f"- {symbol}: {details['shares']} shares @ ${details['avg_price']:,.2f}")
    
    print("\nOptions:")
    print("1. New Investment Analysis")
    print("2. Portfolio Review & Optimization")
    print("3. Query Investment Knowledge")
    mode = input("\nChoose option (1/2/3): ")
    
    if mode == "1":
        analysis = analyze_new_investment(
            user_profile['monthly_investment'],
            user_profile['risk_tolerance'],
            user_id
        )
        print("\nInvestment Analysis:")
        print(analysis)
    
    elif mode == "2":
        review = review_portfolio(user_id)
        print("\nPortfolio Review:")
        print(review)
    
    elif mode == "3":
        query = input("\nWhat would you like to know about investments? ")
        knowledge = query_investment_knowledge(query)
        print("\nInvestment Knowledge:")
        print(knowledge)