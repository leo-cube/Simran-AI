import json
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from langchain.tools import Tool
from typing import Dict, List, Any
from datetime import datetime

def process_investment_data(data: Dict[str, Any]) -> str:
    """Process and visualize investment data"""
    if "portfolio" in data:
        # Process portfolio data
        current_inv = data["portfolio"]["current_investment"]
        new_inv = data["portfolio"].get("new_investment_plan", {})
        
        # Create pie chart for current investment
        fig1 = px.pie(
            names=[stock["name"] for stock in current_inv["stocks"]],
            values=[stock["investment_amount"] for stock in current_inv["stocks"]],
            title="Current Investment Distribution"
        )
        fig1.write_html("current_investment.html")
        
        # Create bar chart for new investment plan if exists
        if new_inv:
            sectors = []
            amounts = []
            for alloc in new_inv["allocation"]:
                sectors.append(alloc["sector"])
                amounts.append(alloc["investment_amount"])
            
            fig2 = px.bar(
                x=sectors,
                y=amounts,
                title="New Investment Plan by Sector"
            )
            fig2.write_html("new_investment.html")
            
        return "Investment visualizations created successfully"
    
    elif "recommended_allocation" in data:
        # Process recommended allocation data
        alloc = data["recommended_allocation"]
        
        fig = px.pie(
            names=[item["investment_type"] for item in alloc],
            values=[item["investment_amount"] for item in alloc],
            title=f"Recommended Investment Allocation (Total: ₹{data['total_funds']})"
        )
        fig.write_html("recommended_allocation.html")
        
        return "Recommendation visualization created successfully"
    
    return "Invalid data format"

def save_investment_data(data: Dict[str, Any], filename: str = None) -> str:
    """Save investment data to JSON file"""
    if not filename:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"investment_data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    
    return f"Data saved to {filename}"

# Create tools
process_investment_tool = Tool(
    name="process_investment_data",
    func=process_investment_data,
    description="Process and visualize investment data in various formats"
)

save_investment_tool = Tool(
    name="save_investment_data",
    func=save_investment_data,
    description="Save investment data to a JSON file"
) 