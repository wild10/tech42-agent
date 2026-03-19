from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from src.config import PINECONE_API_KEY, PINECONE_INDEX_NAME, PINECONE_REGION
from src.rag.embeddings import get_embeddings_models


def init_pinecone():
    """
    create the new  Pinecone vector Space setup
    """
    # connect with Pinecone and instance it.
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Create index if it doesn't exist
    if PINECONE_INDEX_NAME not in pc.list_indexes().names(): 
        pc.create_index(
            name = PINECONE_INDEX_NAME,
            dimension=1536,          # text-embedding-3-small = 1536 dims   
            metric="cosine",
            spec= ServerlessSpec(
                cloud="aws",
                region=PINECONE_REGION,
            )
        )

    return pc 

# Retrieve vectors from Pinecone name
def get_vectorstore():
    """
    Retrieve vectors from Pinecone.
    """
    # check if the Data already exists.
    # and get info about our VDB.
    pc = init_pinecone()
    index = pc.Index(PINECONE_INDEX_NAME)

    embeddings = get_embeddings_models()


    return PineconeVectorStore(
        index= index,
        embedding=embeddings,
    )
