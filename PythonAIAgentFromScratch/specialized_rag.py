from json_rag import JSONRAG
from json_generator import InvestmentJSONGenerator
from typing import Dict, Any, Tuple

class InvestedUserRAG(JSONRAG):
    """RAG system specialized for already invested users."""
    def __init__(self):
        super().__init__("invested_user_data.json")
        self.json_generator = InvestmentJSONGenerator()
    
    def get_personalized_recommendation(self, query: str, user_id: str) -> Tuple[str, Dict[str, Any]]:
        try:
            # Check if query is finance-related
            finance_keywords = self._extract_finance_keywords(query)
            if not finance_keywords:
                return "I can only provide information about investment topics available in our financial database.", {}
            
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
                            Structure your response to include:
                            1. Current portfolio analysis
                            2. Investment recommendations
                            3. Risk metrics
                            4. Tax considerations
                            5. Portfolio rebalancing suggestions"""
                        },
                        {
                            "role": "user", 
                            "content": f"Financial Analysis:\n{base_response}\n\nProvide advanced financial analysis for an experienced investor, using ONLY the provided financial data and metrics."
                        }
                    ],
                    temperature=0.3
                )
                analysis = response.choices[0].message.content
                
                # Extract structured data from the analysis
                structured_data = self._extract_investment_data(analysis)
                
                # Generate JSON output
                json_output = self.json_generator.generate_investment_json(
                    user_type='invested_user',
                    user_id=user_id,
                    investment_data=structured_data
                )
                
                return analysis, json_output
            
            return base_response, {}
        except Exception as e:
            return f"Error analyzing financial data: {str(e)}", {}
    
    def _extract_investment_data(self, analysis: str) -> Dict[str, Any]:
        """Extract structured investment data from analysis text."""
        # This is a placeholder. In a real implementation, you would use
        # NLP techniques to extract structured data from the text.
        return {
            "investment_goal": "Wealth Growth",
            "risk_tolerance": "High",
            "investment_horizon": "Long-term",
            "total_portfolio_value": 100000,
            "current_investment": {
                "total_amount": 75000,
                "allocation": [
                    {
                        "type": "Stocks",
                        "percentage": 60,
                        "amount": 45000,
                        "holdings": ["AAPL", "MSFT", "GOOGL"]
                    },
                    {
                        "type": "Bonds",
                        "percentage": 40,
                        "amount": 30000,
                        "holdings": ["Treasury Bonds", "Corporate Bonds"]
                    }
                ]
            },
            "new_investment": {
                "total_amount": 25000,
                "allocation": [
                    {
                        "type": "ETFs",
                        "percentage": 50,
                        "amount": 12500,
                        "reason": "Diversification"
                    },
                    {
                        "type": "Real Estate",
                        "percentage": 50,
                        "amount": 12500,
                        "reason": "Income generation"
                    }
                ],
                "rationale": ["Market conditions favorable", "Sector rotation needed"]
            },
            "portfolio_analysis": {
                "diversification_score": 0.85,
                "risk_adjusted_return": 0.12
            },
            "risk_metrics": {
                "beta": 1.2,
                "sharpe_ratio": 1.5,
                "max_drawdown": -0.15
            },
            "tax_considerations": [
                "Tax-loss harvesting opportunities",
                "Long-term capital gains"
            ]
        }

class ReadyToInvestRAG(JSONRAG):
    """RAG system specialized for users ready to start investing."""
    def __init__(self):
        super().__init__("ready_to_invest_data.json")
        self.json_generator = InvestmentJSONGenerator()
    
    def get_personalized_recommendation(self, query: str, user_id: str) -> Tuple[str, Dict[str, Any]]:
        try:
            # Check if query is finance-related
            finance_keywords = self._extract_finance_keywords(query)
            if not finance_keywords:
                return "I can only provide information about investment topics available in our financial database.", {}
            
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
                            Structure your response to include:
                            1. Investment goals and risk assessment
                            2. Recommended portfolio allocation
                            3. Implementation strategy
                            4. Monitoring and rebalancing plan
                            5. Next steps"""
                        },
                        {
                            "role": "user", 
                            "content": f"Financial Analysis:\n{base_response}\n\nExplain this financial data for a new investor, using ONLY the provided financial information and metrics."
                        }
                    ],
                    temperature=0.3
                )
                analysis = response.choices[0].message.content
                
                # Extract structured data from the analysis
                structured_data = self._extract_investment_data(analysis)
                
                # Generate JSON output
                json_output = self.json_generator.generate_investment_json(
                    user_type='ready_to_invest',
                    user_id=user_id,
                    investment_data=structured_data
                )
                
                return analysis, json_output
            
            return base_response, {}
        except Exception as e:
            return f"Error analyzing financial data: {str(e)}", {}
    
    def _extract_investment_data(self, analysis: str) -> Dict[str, Any]:
        """Extract structured investment data from analysis text."""
        # This is a placeholder. In a real implementation, you would use
        # NLP techniques to extract structured data from the text.
        return {
            "investment_goal": "Long-term Growth",
            "risk_tolerance": "Medium",
            "investment_horizon": "10+ years",
            "total_funds": 50000,
            "recommended_allocation": [
                {
                    "type": "Index Funds",
                    "percentage": 60,
                    "amount": 30000,
                    "reason": "Core portfolio growth"
                },
                {
                    "type": "Bonds",
                    "percentage": 30,
                    "amount": 15000,
                    "reason": "Stability"
                },
                {
                    "type": "Cash",
                    "percentage": 10,
                    "amount": 5000,
                    "reason": "Emergency fund"
                }
            ],
            "investment_vehicles": [
                {
                    "type": "ETF",
                    "name": "Total Market Index",
                    "allocation": 40,
                    "amount": 20000,
                    "features": ["Low cost", "Broad diversification"],
                    "risks": ["Market risk"]
                }
            ],
            "implementation_strategy": [
                "Open brokerage account",
                "Set up automatic investments",
                "Start with index funds"
            ],
            "monitoring_plan": [
                "Monthly portfolio review",
                "Quarterly rebalancing check"
            ],
            "rebalancing_schedule": {
                "frequency": "Quarterly",
                "threshold": "5% deviation"
            }
        }

class NoIdeaRAG(JSONRAG):
    """RAG system specialized for new investors with no prior experience."""
    def __init__(self):
        super().__init__("no_idea_data.json")
        self.json_generator = InvestmentJSONGenerator()
    
    def get_personalized_recommendation(self, query: str, user_id: str) -> Tuple[str, Dict[str, Any]]:
        try:
            # Check if query is finance-related
            finance_keywords = self._extract_finance_keywords(query)
            if not finance_keywords:
                return "I can only provide information about investment topics available in our financial database.", {}
            
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
                            Structure your response to include:
                            1. Basic investment concepts
                            2. Recommended starter portfolio
                            3. Risk management basics
                            4. Emergency fund setup
                            5. Next steps for getting started"""
                        },
                        {
                            "role": "user", 
                            "content": f"Financial Analysis:\n{base_response}\n\nExplain this financial data in simple terms for a beginner, using ONLY the provided financial information."
                        }
                    ],
                    temperature=0.3
                )
                analysis = response.choices[0].message.content
                
                # Extract structured data from the analysis
                structured_data = self._extract_investment_data(analysis)
                
                # Generate JSON output
                json_output = self.json_generator.generate_investment_json(
                    user_type='new_investor',
                    user_id=user_id,
                    investment_data=structured_data
                )
                
                return analysis, json_output
            
            return base_response, {}
        except Exception as e:
            return f"Error analyzing financial data: {str(e)}", {}
    
    def _extract_investment_data(self, analysis: str) -> Dict[str, Any]:
        """Extract structured investment data from analysis text."""
        # This is a placeholder. In a real implementation, you would use
        # NLP techniques to extract structured data from the text.
        return {
            "investment_goal": "Start Investing",
            "risk_tolerance": "Low",
            "investment_horizon": "5+ years",
            "total_funds": 10000,
            "recommended_allocation": [
                {
                    "type": "Fixed Deposits",
                    "percentage": 40,
                    "amount": 4000,
                    "reason": "Safe and stable returns"
                },
                {
                    "type": "Index Funds",
                    "percentage": 30,
                    "amount": 3000,
                    "reason": "Market exposure with lower risk"
                },
                {
                    "type": "High-Yield Savings",
                    "percentage": 30,
                    "amount": 3000,
                    "reason": "Emergency fund"
                }
            ],
            "emergency_fund": {
                "amount": 3000,
                "bank": "High-yield savings account",
                "reason": "Emergency fund for unexpected expenses"
            },
            "investment_rationale": [
                "Start with low-risk investments",
                "Focus on learning and understanding",
                "Build emergency fund first"
            ],
            "risk_management": [
                "Diversification across asset types",
                "Regular monitoring",
                "Start small and increase gradually"
            ],
            "next_steps": [
                "Open a savings account",
                "Research index funds",
                "Set up automatic savings plan"
            ]
        } 