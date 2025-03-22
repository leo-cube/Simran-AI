from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from typing import Dict, List, Any, Optional, Union
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

# Base search and wiki tools
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for current market information and investment trends",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=100)
wiki_tool = Tool(
    name="wiki",
    func=WikipediaQueryRun(api_wrapper=api_wrapper).run,
    description="Search Wikipedia for information about investment terms and concepts",
)

# Enhanced RAG system with investment focus
class InvestmentRAG:
    def __init__(self):
        self.embeddings = None
        if os.getenv('OPENAI_API_KEY'):
            self.embeddings = OpenAIEmbeddings()
        else:
            print("Warning: OpenAI API key not found. RAG system will use basic text matching.")
        
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        self.vector_store = None
        self.text_data = []  # Fallback storage when no embeddings available
    
    def _convert_to_text(self, data: Dict[str, Any]) -> str:
        """Convert investment data to searchable text format"""
        text = f"Investment Profile - User: {data.get('user_id', 'Unknown')}\n"
        text += f"Goal: {data.get('investment_goal', 'Not specified')}\n"
        
        if 'portfolio' in data:
            portfolio = data['portfolio']
            current = portfolio.get('current_investment', {})
            text += f"\nCurrent Investment: ${current.get('total_invested', 0):,}\n"
            for stock in current.get('stocks', []):
                text += f"- {stock['name']}: {stock['percentage']}% (${stock['investment_amount']:,})\n"
            
            new_plan = portfolio.get('new_investment_plan', {})
            if new_plan:
                text += f"\nNew Investment Plan: ${new_plan.get('total_new_investment', 0):,}\n"
                for alloc in new_plan.get('allocation', []):
                    text += f"- {alloc['sector']}: ${alloc['investment_amount']:,}\n"
        
        if 'recommended_allocation' in data:
            text += f"\nRecommended Allocation (Total: ${data.get('total_funds', 0):,})\n"
            for alloc in data['recommended_allocation']:
                text += f"- {alloc['investment_type']}: ${alloc['investment_amount']:,}"
                if 'reason' in alloc:
                    text += f" ({alloc['reason']})"
                text += "\n"
        
        return text
    
    def add_data(self, data: Union[Dict[str, Any], List[Dict[str, Any]]]) -> str:
        """Add investment data to the RAG system"""
        if isinstance(data, list):
            texts = [self._convert_to_text(item) for item in data]
        else:
            texts = [self._convert_to_text(data)]
        
        if self.embeddings:
            docs = self.text_splitter.create_documents(texts)
            if self.vector_store is None:
                self.vector_store = FAISS.from_documents(docs, self.embeddings)
            else:
                self.vector_store.add_documents(docs)
        else:
            self.text_data.extend(texts)
        
        return f"Added {len(texts)} investment profile(s) to RAG system"
    
    def query(self, query: str) -> str:
        """Query the RAG system for relevant investment insights"""
        if self.embeddings and self.vector_store:
            relevant_docs = self.vector_store.similarity_search(query, k=3)
            return "\n\n---\n\n".join(doc.page_content for doc in relevant_docs)
        elif self.text_data:
            # Fallback: keyword matching with context
            matching_data = []
            query_terms = query.lower().split()
            for text in self.text_data:
                relevance_score = sum(term in text.lower() for term in query_terms)
                if relevance_score > 0:
                    matching_data.append((relevance_score, text))
            
            if matching_data:
                # Sort by relevance and return top 3
                matching_data.sort(reverse=True)
                return "\n\n---\n\n".join(text for _, text in matching_data[:3])
            return "No relevant investment profiles found"
        else:
            return "No investment data available in RAG system"

rag_system = InvestmentRAG()

# Enhanced visualization tool
def create_investment_visualization(data: Dict[str, Any], viz_type: str = "default") -> str:
    """Create interactive investment visualizations using Plotly"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if "portfolio" in data:
            # Create multiple visualizations for portfolio analysis
            figs = []
            
            # Current investment distribution
            if "current_investment" in data["portfolio"]:
                current = data["portfolio"]["current_investment"]
                fig1 = px.pie(
                    names=[s["name"] for s in current["stocks"]],
                    values=[s["investment_amount"] for s in current["stocks"]],
                    title="Current Investment Distribution"
                )
                figs.append(("current", fig1))
            
            # New investment plan
            if "new_investment_plan" in data["portfolio"]:
                new_plan = data["portfolio"]["new_investment_plan"]
                sectors = []
                amounts = []
                for alloc in new_plan["allocation"]:
                    sectors.append(alloc["sector"])
                    amounts.append(alloc["investment_amount"])
                
                fig2 = go.Figure(data=[
                    go.Bar(
                        x=sectors,
                        y=amounts,
                        text=[f"${a:,}" for a in amounts],
                        textposition='auto',
                    )
                ])
                fig2.update_layout(
                    title="New Investment Plan by Sector",
                    yaxis_title="Investment Amount ($)",
                    showlegend=False
                )
                figs.append(("new_plan", fig2))
            
            # Save all figures
            paths = []
            for name, fig in figs:
                filename = f"investment_{name}_{timestamp}.html"
                fig.write_html(filename)
                paths.append(filename)
            
            return json.dumps(paths)
            
        elif "recommended_allocation" in data:
            # Create visualization for recommended allocation
            alloc = data["recommended_allocation"]
            fig = px.pie(
                names=[item["investment_type"] for item in alloc],
                values=[item["investment_amount"] for item in alloc],
                title=f"Recommended Investment Allocation (Total: ${data['total_funds']:,})"
            )
            
            filename = f"recommended_allocation_{timestamp}.html"
            fig.write_html(filename)
            return json.dumps([filename])
            
        return json.dumps(["Unsupported data format for visualization"])
    except Exception as e:
        return json.dumps([f"Error creating visualization: {str(e)}"])

# Create tools
dynamic_rag_tool = Tool(
    name="dynamic_rag",
    func=rag_system.add_data,
    description="Add investment data to the RAG system for future reference. Input can be a single investment profile or a list of profiles."
)

rag_query_tool = Tool(
    name="rag_query",
    func=rag_system.query,
    description="Query the RAG system for relevant investment insights based on user's query."
)

visualization_tool = Tool(
    name="visualization",
    func=create_investment_visualization,
    description="Create interactive visualizations of investment data. Returns a list of HTML file paths."
)

# Save tool
def save_data(data: Any, filename: Optional[str] = None) -> str:
    """Save any data to a file"""
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"investment_data_{timestamp}.json"
    
    try:
        with open(filename, 'w') as f:
            if isinstance(data, (dict, list)):
                json.dump(data, f, indent=2)
            else:
                f.write(str(data))
        return f"Data saved to {filename}"
    except Exception as e:
        return f"Error saving data: {str(e)}"

save_tool = Tool(
    name="save",
    func=save_data,
    description="Save investment data to a file"
) 