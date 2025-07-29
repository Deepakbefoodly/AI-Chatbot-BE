import google.generativeai as genai
import time
import config

genai.configure(api_key=config.GEMINI_API_KEY)

batch_size: int = 5
delay: float = 1.0

def generate_embeddings(text_chunks):
    embedding_response = []
    model = genai.embed_content

    # embedding in batches to avoid rate limit error
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]

        for chunk in batch:
            try:
                response = model(
                    model="models/embedding-001",
                    content=chunk,
                    task_type="retrieval_document"
                )
                embedding_response.append(response["embedding"])
            except Exception as e:
                raise e

        # Wait between batches
        if i + batch_size < len(text_chunks):
            time.sleep(delay)

    return embedding_response

def embed_text(text):
    model = genai.embed_content
    return model(model="models/embedding-001", content=text, task_type="retrieval_document")["embedding"]