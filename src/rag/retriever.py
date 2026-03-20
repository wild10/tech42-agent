from src.rag.vectorstore import get_vectorstore
from src.core.config import PINECONE_INDEX_NAME
# # inicializar UNA VEZ (singleton simple)
# _vectorstore = get_vectorstore()

# print(f"vector DB found: ->: {_vectorstore.index.name}")
# print(f"vector DB found: ->: {_vectorstore.embeddings.model_name}")

# def get_retriever(k: int = 5):
#     """
#     Retrieve top-k similar chunks from Pinecone
#     """

#     return _vectorstore.as_retriever(
#         search_type="similarity",  # conse -similarities.
#         search_kwargs={"k": k}
#     )

def get_retriever(k: int = 5):
    """
    Retrieve the most similar vectors top k= 5
    """
    vectostore = get_vectorstore()

    # indexes = vectostore.list_indexes().names()
    # if PINECONE_INDEX_NAME not in indexes:
    #     raise ValueError(f"Index {PINECONE_INDEX_NAME} not found")
    # else:
    #     print(f"vector DB found: ->: {vectostore.index.name}")
    

    return vectostore.as_retriever(
        search_kwargs={"k":k}
    )
