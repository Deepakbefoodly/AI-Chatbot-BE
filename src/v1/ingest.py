import requests, re
from src.v1.vector_store import add_documents
import nltk

# from openai_utils.service import generate_embeddings
from src.v1.gemini_utils.service import generate_embeddings
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup
from src.v1.chroma_db.data_scraper import get_child_urls, get_byte_size, split_text_by_bytes

MAX_BYTES = 16000

def fetch_gitlab_docs():
    parent_urls = [
        "https://handbook.gitlab.com/handbook"
    ]

    child_urls = get_child_urls(parent_urls)

    texts = []
    for url in child_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style", 'header', 'nav', 'aside', '.sidebar', '.navbar', '#header', '#sidebar']):
            script.decompose()

        # Extract text content
        text = soup.get_text()

        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        clean_text = '\n'.join(line for line in lines if line)

        texts.append(clean_text.strip())

    return texts

def chunk_text(text, chunk_size=350):
    sentences = sent_tokenize(text)
    chunks, chunk = [], ""
    for sent in sentences:
        if len(chunk) + len(sent) < chunk_size:
            chunk += " " + sent
        else:
            if get_byte_size(chunk) > MAX_BYTES:
                print("sad")
            chunks.append(chunk.strip())
            chunk = sent
    if chunk:
        chunks.append(chunk.strip())

    return chunks

def ingest():
    nltk.download("punkt_tab")
    docs = fetch_gitlab_docs()
    smaller_docs = []

    for doc in docs:
        if get_byte_size(doc) > MAX_BYTES:
            smaller_docs.extend(split_text_by_bytes(doc, MAX_BYTES))
        else:
            smaller_docs.append(doc)

    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))

    embeddings = generate_embeddings(all_chunks)
    add_documents(all_chunks, embeddings)

if __name__ == "__main__":
    ingest()
