from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.tools import Tool
from typing import List, Dict, Any
import json

class InvestmentRAG:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50
        )
        self.vector_store = None
        
    def add_investment_data(self, data: List[Dict[str, Any]]) -> str:
        """Add investment data to the RAG system"""
        texts = []
        for item in data:
            texts.append(json.dumps(item, indent=2))
        
        docs = self.text_splitter.create_documents(texts)
        
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(docs, self.embeddings)
        else:
            self.vector_store.add_documents(docs)
        
        return f"Added {len(docs)} documents to the RAG system"
    
    def query_investment_knowledge(self, query: str) -> str:
        """Query the RAG system for investment knowledge"""
        if self.vector_store is None:
            return "No investment data available in the RAG system"
        
        relevant_docs = self.vector_store.similarity_search(query, k=3)
        
        result = "Relevant investment information:\n\n"
        for i, doc in enumerate(relevant_docs, 1):
            result += f"{i}. {doc.page_content}\n\n"
        
        return result

# Initialize RAG system
rag_system = InvestmentRAG()

# Create tools
add_investment_knowledge_tool = Tool(
    name="add_investment_knowledge",
    func=rag_system.add_investment_data,
    description="Add investment data to the RAG system for future reference"
)

query_investment_knowledge_tool = Tool(
    name="query_investment_knowledge",
    func=rag_system.query_investment_knowledge,
    description="Query the RAG system for relevant investment knowledge"
) 