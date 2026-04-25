import requests, re
from src.v1.vector_store import add_documents
import nltk

# from openai_utils.service import generate_embeddings
from src.v1.gemini_utils.service import generate_embeddings
from nltk.tokenize import sent_tokenize
from src.v1.chroma_db.data_scraper import fetch_gitlab_docs, get_byte_size, split_text_by_bytes
from src.v1.common_utils import save_chunks, load_chunks

MAX_BYTES = 16000

def chunk_text(text, chunk_size=500):
    sentences = sent_tokenize(text)
    chunks, chunk = [], ""
    for sent in sentences:
        if len(chunk) + len(sent) < chunk_size:
            chunk += " " + sent
        else:
            chunks.append(chunk.strip())
            chunk = sent
    if chunk:
        chunks.append(chunk.strip())

    return chunks

def ingest():
    nltk.download("punkt_tab")
    cache_chunks = load_chunks()
    if not cache_chunks:
        docs = fetch_gitlab_docs()
        smaller_docs = []

        for doc in docs:
            if get_byte_size(doc) > MAX_BYTES:
                smaller_docs.extend(split_text_by_bytes(doc, MAX_BYTES))
            else:
                smaller_docs.append(doc)

        all_chunks = []
        for doc in smaller_docs:
            all_chunks.extend(chunk_text(doc))

        save_chunks(all_chunks)
        cache_chunks = all_chunks

    embeddings = generate_embeddings(cache_chunks[500:600])
    add_documents(cache_chunks[500:600], embeddings)

if __name__ == "__main__":
    ingest()
