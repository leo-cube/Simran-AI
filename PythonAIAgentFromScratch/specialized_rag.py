from json_rag import JSONRAG
from typing import Dict, List, Optional

class InvestedUserRAG(JSONRAG):
    """RAG system specialized for already invested users."""
    def __init__(self):
        super().__init__("invested_user_data.json")
        self.user_type = "invested_user"
    
    def get_personalized_recommendation(self, query: str) -> str:
        """Get personalized recommendations for invested users."""
        base_response = self.query(query)
        
        # Add specialized context for invested users
        specialized_context = """
        As an experienced investor, you have access to:
        - Advanced portfolio optimization strategies
        - Technical and fundamental analysis tools
        - Risk management techniques
        - Market analysis capabilities
        """
        
        return f"""
        {base_response}
        
        {specialized_context}
        
        Note: This recommendation is tailored for experienced investors with existing portfolios.
        """

class ReadyToInvestRAG(JSONRAG):
    """RAG system specialized for users ready to start investing."""
    def __init__(self):
        super().__init__("ready_to_invest_data.json")
        self.user_type = "ready_to_invest"
    
    def get_personalized_recommendation(self, query: str) -> str:
        """Get personalized recommendations for users ready to invest."""
        base_response = self.query(query)
        
        # Add specialized context for ready-to-invest users
        specialized_context = """
        As someone ready to start investing, you should focus on:
        - Understanding basic investment concepts
        - Setting clear investment goals
        - Learning about risk management
        - Developing a research strategy
        """
        
        return f"""
        {base_response}
        
        {specialized_context}
        
        Note: This recommendation is tailored for new investors ready to enter the market.
        """

class NoIdeaRAG(JSONRAG):
    """RAG system specialized for new investors with no prior experience."""
    def __init__(self):
        super().__init__("no_idea_data.json")
        self.user_type = "no_idea"
    
    def get_personalized_recommendation(self, query: str) -> str:
        """Get personalized recommendations for new investors."""
        base_response = self.query(query)
        
        # Add specialized context for new investors
        specialized_context = """
        As a new investor, you should focus on:
        - Learning basic investment concepts
        - Understanding different investment types
        - Setting realistic goals
        - Starting with educational resources
        """
        
        return f"""
        {base_response}
        
        {specialized_context}
        
        Note: This recommendation is tailored for new investors learning about the market.
        """ 