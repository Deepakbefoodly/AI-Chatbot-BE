import requests, re
import vector_store
import nltk

# from openai_utils.service import generate_embeddings
from gemini_utils.service import generate_embeddings
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup

def fetch_gitlab_docs():
    urls = [
        "https://about.gitlab.com/direction/",

    ]
    texts = []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Extract text content
        text = soup.get_text()

        # Clean up text
        lines = (line.strip() for line in text.splitlines())
        clean_text = '\n'.join(line for line in lines if line)

        texts.append(clean_text.strip())

    return texts

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
    docs = fetch_gitlab_docs()
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))
    embeddings = generate_embeddings(all_chunks)
    vector_store.add_documents(all_chunks, embeddings)

if __name__ == "__main__":
    ingest()
