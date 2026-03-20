from langchain.tools import tool
from src.rag.retriever import get_retriever

@tool
def retrieve_doc(query: str):
    """
    Search and retrieve relevant information from Amazon's official financial knowledge base 
    (2024 Annual Report, Q2/Q3 2025 Earnings Releases). 
    Use this for metrics, corporate strategy, AI business (AWS), and office space information.
    """
    retriever = get_retriever()
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])