
from src.rag.vectorstore import get_vectorstore


## Ingestion procedure:
def ingest_chunks(chunks: list[dict]):

    # get info about vector DB and embeddings.
    vectorstore = get_vectorstore()
    texts = [chunk["content"] for chunk in chunks ]
    metadatas = [ chunk.get("metadata",{})  for chunk in chunks ]

    vectorstore.add_texts(
        texts= texts,
        metadatas= metadatas
    )

    print(f"Ingested {len(texts)} chunks into Pinecone")



"""
another funcion for batch ingestion. no used now
"""
def ingest_chunks_batches(chunks: list[dict], batch_size: int = 50):

    vectorstore = get_vectorstore()

    total = len(chunks)

    for i in range(0, total, batch_size):
        batch = chunks[i:i + batch_size]

        texts = [chunk["content"] for chunk in batch]
        metadatas = [chunk.get("metadata", {}) for chunk in batch]

        vectorstore.add_texts(
            texts=texts,
            metadatas=metadatas
        )

        print(f"Batch {i//batch_size + 1} ingested ({len(texts)} chunks)")

    print(f"Total ingested: {total} chunks")