from src.rag.retriever import get_retriever


def retrieve_context(query: str):
    """
    retrieve the context information 
    """
    # get similairty vectors.
    retriever = get_retriever()
    docs = retriever.invoke(query)
   
    print(f"Retrieved {len(docs)} documents")
   
    return [doc.page_content for doc in docs]


