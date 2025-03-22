from typing import Dict, List, Any, Optional
import json

class InvestmentJSONGenerator:
    def __init__(self):
        self.user_types = {
            'new_investor': self._generate_new_investor_json,
            'ready_to_invest': self._generate_ready_investor_json,
            'invested_user': self._generate_invested_user_json
        }
    
    def generate_investment_json(self, 
                               user_type: str,
                               user_id: str,
                               investment_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate structured JSON based on user type and investment data."""
        if user_type not in self.user_types:
            raise ValueError(f"Invalid user type: {user_type}")
        
        return self.user_types[user_type](user_id, investment_data)
    
    def _generate_new_investor_json(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON structure for new investors."""
        return {
            "user_id": user_id,
            "investment_profile": {
                "goal": data.get("investment_goal", ""),
                "risk_tolerance": data.get("risk_tolerance", "Low"),
                "investment_horizon": data.get("investment_horizon", ""),
                "total_funds": data.get("total_funds", 0)
            },
            "new_investment_plan": {
                "total_amount": data.get("total_funds", 0),
                "allocation": self._generate_allocation(data.get("recommended_allocation", [])),
                "emergency_fund": {
                    "amount": data.get("emergency_fund", {}).get("amount", 0),
                    "bank": data.get("emergency_fund", {}).get("bank", ""),
                    "reason": "Emergency fund for unexpected expenses"
                }
            },
            "investment_rationale": data.get("investment_rationale", []),
            "risk_management": data.get("risk_management", []),
            "next_steps": data.get("next_steps", []),
            "visualizations": {
                "allocation_chart": {
                    "type": "pie",
                    "title": "Recommended Investment Allocation",
                    "data": [
                        {
                            "label": alloc.get("type", ""),
                            "value": alloc.get("percentage", 0),
                            "color": self._get_chart_color(idx)
                        }
                        for idx, alloc in enumerate(data.get("recommended_allocation", []))
                    ]
                },
                "risk_education": {
                    "type": "bar",
                    "title": "Risk vs Return Basics",
                    "data": [
                        {"label": "Fixed Deposits", "risk": 1, "return": 2},
                        {"label": "Index Funds", "risk": 3, "return": 4},
                        {"label": "High-Yield Savings", "risk": 1, "return": 2}
                    ],
                    "axes": {
                        "x": "Investment Type",
                        "y": "Risk/Return Level (1-5)"
                    }
                },
                "emergency_fund": {
                    "type": "gauge",
                    "title": "Emergency Fund Progress",
                    "data": {
                        "current": data.get("emergency_fund", {}).get("amount", 0),
                        "target": data.get("total_funds", 0) * 0.3,
                        "colors": ["red", "yellow", "green"]
                    }
                }
            }
        }
    
    def _generate_ready_investor_json(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON structure for users ready to invest."""
        return {
            "user_id": user_id,
            "investment_profile": {
                "goal": data.get("investment_goal", ""),
                "risk_tolerance": data.get("risk_tolerance", "Medium"),
                "investment_horizon": data.get("investment_horizon", ""),
                "total_funds": data.get("total_funds", 0)
            },
            "portfolio": {
                "total_amount": data.get("total_funds", 0),
                "allocation": self._generate_allocation(data.get("recommended_allocation", [])),
                "investment_vehicles": self._generate_investment_vehicles(data.get("investment_vehicles", []))
            },
            "implementation_strategy": data.get("implementation_strategy", []),
            "monitoring_plan": data.get("monitoring_plan", []),
            "rebalancing_schedule": data.get("rebalancing_schedule", {}),
            "visualizations": {
                "portfolio_allocation": {
                    "type": "donut",
                    "title": "Proposed Portfolio Allocation",
                    "data": [
                        {
                            "label": alloc.get("type", ""),
                            "value": alloc.get("percentage", 0),
                            "color": self._get_chart_color(idx)
                        }
                        for idx, alloc in enumerate(data.get("recommended_allocation", []))
                    ]
                },
                "risk_return_spectrum": {
                    "type": "scatter",
                    "title": "Risk-Return Analysis",
                    "data": [
                        {
                            "label": vehicle.get("name", ""),
                            "risk": self._calculate_risk_score(vehicle),
                            "return": self._calculate_return_potential(vehicle)
                        }
                        for vehicle in data.get("investment_vehicles", [])
                    ],
                    "axes": {
                        "x": "Risk Level",
                        "y": "Expected Return"
                    }
                },
                "implementation_timeline": {
                    "type": "timeline",
                    "title": "Investment Implementation Plan",
                    "data": [
                        {
                            "phase": f"Phase {idx + 1}",
                            "action": step,
                            "duration": f"Week {idx + 1}"
                        }
                        for idx, step in enumerate(data.get("implementation_strategy", []))
                    ]
                }
            }
        }
    
    def _generate_invested_user_json(self, user_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate JSON structure for experienced investors."""
        return {
            "user_id": user_id,
            "investment_profile": {
                "goal": data.get("investment_goal", ""),
                "risk_tolerance": data.get("risk_tolerance", "High"),
                "investment_horizon": data.get("investment_horizon", ""),
                "total_portfolio_value": data.get("total_portfolio_value", 0)
            },
            "current_investment": {
                "total_amount": data.get("current_investment", {}).get("total_amount", 0),
                "allocation": self._generate_current_allocation(data.get("current_investment", {}).get("allocation", []))
            },
            "new_investment_plan": {
                "total_amount": data.get("new_investment", {}).get("total_amount", 0),
                "allocation": self._generate_allocation(data.get("new_investment", {}).get("allocation", [])),
                "rationale": data.get("new_investment", {}).get("rationale", [])
            },
            "portfolio_analysis": data.get("portfolio_analysis", {}),
            "risk_metrics": data.get("risk_metrics", {}),
            "tax_considerations": data.get("tax_considerations", []),
            "visualizations": {
                "current_vs_proposed": {
                    "type": "stacked_bar",
                    "title": "Current vs Proposed Allocation",
                    "data": {
                        "current": [
                            {
                                "label": alloc.get("type", ""),
                                "value": alloc.get("percentage", 0),
                                "color": self._get_chart_color(idx)
                            }
                            for idx, alloc in enumerate(data.get("current_investment", {}).get("allocation", []))
                        ],
                        "proposed": [
                            {
                                "label": alloc.get("type", ""),
                                "value": alloc.get("percentage", 0),
                                "color": self._get_chart_color(idx)
                            }
                            for idx, alloc in enumerate(data.get("new_investment", {}).get("allocation", []))
                        ]
                    }
                },
                "performance_metrics": {
                    "type": "line",
                    "title": "Portfolio Performance Metrics",
                    "data": {
                        "metrics": ["Return", "Risk", "Sharpe Ratio"],
                        "current": [
                            data.get("portfolio_analysis", {}).get("risk_adjusted_return", 0),
                            data.get("risk_metrics", {}).get("beta", 0),
                            data.get("risk_metrics", {}).get("sharpe_ratio", 0)
                        ],
                        "benchmark": [0.10, 1.0, 1.0]
                    }
                },
                "risk_analysis": {
                    "type": "radar",
                    "title": "Risk Analysis",
                    "data": {
                        "dimensions": [
                            "Market Risk",
                            "Credit Risk",
                            "Liquidity Risk",
                            "Concentration Risk",
                            "Currency Risk"
                        ],
                        "values": [
                            data.get("risk_metrics", {}).get("beta", 0),
                            0.7,  # Example credit risk score
                            0.8,  # Example liquidity risk score
                            0.6,  # Example concentration risk score
                            0.4   # Example currency risk score
                        ]
                    }
                }
            }
        }
    
    def _get_chart_color(self, index: int) -> str:
        """Get color for chart elements based on index."""
        colors = [
            "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4",
            "#FFEEAD", "#D4A5A5", "#9B59B6", "#3498DB"
        ]
        return colors[index % len(colors)]
    
    def _calculate_risk_score(self, vehicle: Dict[str, Any]) -> float:
        """Calculate risk score for investment vehicle."""
        risk_factors = {
            "Market risk": 0.4,
            "Volatility": 0.3,
            "Liquidity risk": 0.3
        }
        # Placeholder calculation - would be more sophisticated in real implementation
        return sum(risk_factors.values()) * len(vehicle.get("risks", []))
    
    def _calculate_return_potential(self, vehicle: Dict[str, Any]) -> float:
        """Calculate return potential for investment vehicle."""
        # Placeholder calculation - would be more sophisticated in real implementation
        return vehicle.get("allocation", 0) * 0.1  # 10% expected return
    
    def _generate_allocation(self, allocations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate structured allocation data."""
        structured_allocations = []
        for alloc in allocations:
            structured_alloc = {
                "type": alloc.get("type", ""),
                "percentage": alloc.get("percentage", 0),
                "amount": alloc.get("amount", 0),
                "reason": alloc.get("reason", "")
            }
            
            if "investments" in alloc:
                structured_alloc["investments"] = alloc["investments"]
            
            if "sectors" in alloc:
                structured_alloc["sectors"] = alloc["sectors"]
            
            structured_allocations.append(structured_alloc)
        
        return structured_allocations
    
    def _generate_current_allocation(self, allocations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate structured current allocation data."""
        return [
            {
                "type": alloc.get("type", ""),
                "percentage": alloc.get("percentage", 0),
                "amount": alloc.get("amount", 0),
                "holdings": alloc.get("holdings", [])
            }
            for alloc in allocations
        ]
    
    def _generate_investment_vehicles(self, vehicles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Generate structured investment vehicle data."""
        return [
            {
                "type": vehicle.get("type", ""),
                "name": vehicle.get("name", ""),
                "allocation": vehicle.get("allocation", 0),
                "amount": vehicle.get("amount", 0),
                "features": vehicle.get("features", []),
                "risks": vehicle.get("risks", [])
            }
            for vehicle in vehicles
        ] 