from chroma_db.chroma_connection import get_chroma_collection


collection = get_chroma_collection()

def add_documents(chunks: list[str], embeddings: list[list[float]]):
    ids = [f"doc_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)

def query_similar_docs(query_embedding: list[float], k: int = 3):
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results["documents"][0]
