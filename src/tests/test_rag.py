import logging

from src.rag.embeddings import embed_chunks
from src.rag.ingest import ingest_chunks
from src.rag.loader import load_pdfs
from src.rag.pipeline import retrieve_context
from src.rag.splitter import split_documents


def test_rag():
    # load documents.
    my_docs = load_pdfs("data/pdfs")
    print(f"Loaded {len(my_docs)} documents")

    # Spliting docs in chunks.
    print("Splitting documents...")
    chunks = split_documents(my_docs)
    print(f"Generated {len(chunks)} chunks")
    # # show chunks and its details.
    # for i, chunk in enumerate(chunks[:2]):
    #     print(chunk["content"], chunk["metadata"])

    # generate vectors
    vectors = embed_chunks(chunks[:2])

    print(f"total vectors generated: {len(vectors)}")
    print(f"vector example [0]: {vectors[0]}")

    # ingest chunks
    print(" Ingesting into Pinecone ...")
    ingest_chunks(chunks)

    print("chunks were ingested, check Pinecone!")
    



def test_pipe(query: str):
    result = retrieve_context(query)
    print(result)


if __name__=="__main__":
    # test_rag()

    human_query = "Compare Amazon's recent stock performance to what analysts predicted in their reports"
    test_pipe(human_query)

## running this module: using module "-m"
# >> poetry run python -m src.main
# 