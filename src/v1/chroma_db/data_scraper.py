import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def get_all_links(base_url: str) -> set:
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        if href.startswith(base_url):
            links.add(href.split("#")[0])  # Remove anchor parts
    return links

def get_child_urls(parent_urls: list[str]) -> set:
    child_urls = set()

    for url in parent_urls:
        if url in child_urls:
            continue

        child_urls.update(get_all_links(url))

    return child_urls

def get_byte_size(text: str) -> int:
    return len(text.encode('utf-8'))

def split_text_by_bytes(text: str, max_bytes: int) -> list[str]:
    chunks = []
    current_chunk = ""

    for paragraph in text.split("\n\n"):  # or use sentence tokenizer
        paragraph = paragraph.strip()
        if not paragraph:
            continue

        encoded_paragraph = paragraph.encode('utf-8')
        if len(encoded_paragraph) > max_bytes:
            # Recursively split large paragraph (fallback)
            mid = len(paragraph) // 2
            chunks += split_text_by_bytes(paragraph[:mid], max_bytes)
            chunks += split_text_by_bytes(paragraph[mid:], max_bytes)
        else:
            current_chunk_candidate = (current_chunk + "\n\n" + paragraph).strip()
            if get_byte_size(current_chunk_candidate) <= max_bytes:
                current_chunk = current_chunk_candidate
            else:
                chunks.append(current_chunk)
                current_chunk = paragraph

    if current_chunk:
        chunks.append(current_chunk)

    return chunks
