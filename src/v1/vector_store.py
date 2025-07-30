import uuid

from src.v1.chroma_db.chroma_connection import get_chroma_collection

collection = get_chroma_collection()

batch_size = 300

def add_documents(chunks: list[str], embeddings: list[list[float]]):
    for i in range(0, len(chunks), batch_size):
        batch_chunks = chunks[i:i + batch_size]
        batch_embeddings = embeddings[i:i + batch_size]
        batch_ids = [str(uuid.uuid4()) for _ in batch_chunks]

        try:
            collection.add(documents=batch_chunks, embeddings=batch_embeddings, ids=batch_ids)
        except Exception as ex:
            continue

def query_similar_docs(query_embedding: list[float], k: int = 5):
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results["documents"][0]
