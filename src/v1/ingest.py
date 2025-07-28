import requests, re
import vector_store

from openai.service import generate_embeddings
from nltk.tokenize import sent_tokenize

def fetch_gitlab_docs():
    urls = [
        "https://about.gitlab.com/handbook/engineering/",
        "https://about.gitlab.com/direction/"
    ]
    texts = []
    for url in urls:
        html = requests.get(url).text
        clean_text = re.sub("<[^<]+?>", "", html)  # Strip HTML tags
        texts.append(clean_text)
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
    docs = fetch_gitlab_docs()
    all_chunks = []
    for doc in docs:
        all_chunks.extend(chunk_text(doc))
    embeddings = generate_embeddings(all_chunks)
    vector_store.add_documents(all_chunks, embeddings)

if __name__ == "__main__":
    ingest()
