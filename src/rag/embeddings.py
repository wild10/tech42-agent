from langchain_openai import OpenAIEmbeddings

from src.core.config import OPEN_API_KEY


def get_embeddings_models():
    """
    Create and return the embedding model OpenAI.
    """
    return OpenAIEmbeddings(
        model = "text-embedding-3-small",
        api_key=OPEN_API_KEY,
        # request_timeout=60, # Algunas versiones usan esto
    )

def embed_chunks(chunks: list[dict]) -> list[list[float]]:
    """
    Recieve list of chunks and return list of fectors.
    """

    # Embedding call function.
    embeddings_model = get_embeddings_models()
    # Get the text only from chunks.
    texts = [chunk["content"] for chunk in chunks]
    # turn the text into vector representation.
    vectors = embeddings_model.embed_documents(texts)

    return vectors