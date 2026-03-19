from langchain.tools import tool
from src.rag.retriever import get_retriever

@tool
def retrieve_docs(query: str):
    """
    Search and retrieve relevant information from the knowledge base (Pinecone) 
    based on the user's query. Useful for answering questions about tech42 and its services.
    """
    retriever = get_retriever()
    docs = retriever.invoke(query)
    return "\n\n".join([doc.page_content for doc in docs])

def get_tools():
    """
    Returns a list of tools available for the agent.
    """
    return [retrieve_docs]
