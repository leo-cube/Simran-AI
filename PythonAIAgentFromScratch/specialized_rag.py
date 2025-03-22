from json_rag import JSONRAG
from typing import Dict, Any

class InvestedUserRAG(JSONRAG):
    """RAG system specialized for already invested users."""
    def __init__(self):
        super().__init__("invested_user_data.json")
    
    def get_personalized_recommendation(self, query: str) -> str:
        try:
            # Check if query is finance-related
            finance_keywords = self._extract_finance_keywords(query)
            if not finance_keywords:
                return "I can only provide information about investment topics available in our financial database."
            
            # Get base response using parent class query method
            base_response = self.query(query)
            
            # Add personalized context for invested users
            if self.client:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system", 
                            "content": """You are analyzing financial data for an experienced investor.
                            ONLY use the provided financial data, market information, and stock metrics.
                            DO NOT add any external knowledge or general advice.
                            If specific financial information is not in the context, say 'This financial data is not available in our database.'
                            Focus on advanced financial analysis, technical metrics, and market data present in the context.
                            Analyze the data in terms an experienced investor would understand."""
                        },
                        {
                            "role": "user", 
                            "content": f"Financial Analysis:\n{base_response}\n\nProvide advanced financial analysis for an experienced investor, using ONLY the provided financial data and metrics."
                        }
                    ],
                    temperature=0.3
                )
                return response.choices[0].message.content
            
            return base_response
        except Exception as e:
            return f"Error analyzing financial data: {str(e)}"

class ReadyToInvestRAG(JSONRAG):
    """RAG system specialized for users ready to start investing."""
    def __init__(self):
        super().__init__("ready_to_invest_data.json")
    
    def get_personalized_recommendation(self, query: str) -> str:
        try:
            # Check if query is finance-related
            finance_keywords = self._extract_finance_keywords(query)
            if not finance_keywords:
                return "I can only provide information about investment topics available in our financial database."
            
            # Get base response using parent class query method
            base_response = self.query(query)
            
            # Add personalized context for ready-to-invest users
            if self.client:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system", 
                            "content": """You are analyzing financial data for someone ready to start investing.
                            ONLY use the provided financial data, market information, and stock metrics.
                            DO NOT add any external knowledge or general advice.
                            If specific financial information is not in the context, say 'This financial data is not available in our database.'
                            Focus on explaining basic financial metrics and market data in the context.
                            Break down complex financial terms and provide context for the numbers."""
                        },
                        {
                            "role": "user", 
                            "content": f"Financial Analysis:\n{base_response}\n\nExplain this financial data for a new investor, using ONLY the provided financial information and metrics."
                        }
                    ],
                    temperature=0.3
                )
                return response.choices[0].message.content
            
            return base_response
        except Exception as e:
            return f"Error analyzing financial data: {str(e)}"

class NoIdeaRAG(JSONRAG):
    """RAG system specialized for new investors with no prior experience."""
    def __init__(self):
        super().__init__("no_idea_data.json")
    
    def get_personalized_recommendation(self, query: str) -> str:
        try:
            # Check if query is finance-related
            finance_keywords = self._extract_finance_keywords(query)
            if not finance_keywords:
                return "I can only provide information about investment topics available in our financial database."
            
            # Get base response using parent class query method
            base_response = self.query(query)
            
            # Add personalized context for complete beginners
            if self.client:
                response = self.client.chat.completions.create(
                    model="gpt-4",
                    messages=[
                        {
                            "role": "system", 
                            "content": """You are analyzing financial data for a complete beginner.
                            ONLY use the provided financial data, market information, and stock metrics.
                            DO NOT add any external knowledge or general advice.
                            If specific financial information is not in the context, say 'This financial data is not available in our database.'
                            Focus on explaining basic financial concepts using simple terms.
                            Define any financial terms used and provide context for numbers."""
                        },
                        {
                            "role": "user", 
                            "content": f"Financial Analysis:\n{base_response}\n\nExplain this financial data in simple terms for a beginner, using ONLY the provided financial information."
                        }
                    ],
                    temperature=0.3
                )
                return response.choices[0].message.content
            
            return base_response
        except Exception as e:
            return f"Error analyzing financial data: {str(e)}" 