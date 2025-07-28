import chromadb
from chromadb.config import Settings
import config

client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory="./chroma_db"))
collection = client.get_or_create_collection(config.CHROMA_COLLECTION_NAME)

def add_documents(chunks: list[str], embeddings: list[list[float]]):
    ids = [f"doc_{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)

def query_similar_docs(query_embedding: list[float], k: int = 3):
    results = collection.query(query_embeddings=[query_embedding], n_results=k)
    return results["documents"][0]
