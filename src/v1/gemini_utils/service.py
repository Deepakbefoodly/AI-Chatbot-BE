from google import genai
import time
from src.config import GEMINI_API_KEY
from src.v1.schemas import StreamRequestGemini

client = genai.Client(api_key=GEMINI_API_KEY)

batch_size: int = 20
delay: float = 7.0

def generate_embeddings(text_chunks, retries=3):
    embedding_response = []

    for i in range(0, len(text_chunks), batch_size):
        try:
        # embedding in batches to avoid rate limit error

            batch = [c for c in text_chunks[i:i + batch_size] if c.strip()]

            response = client.models.embed_content(
                model="gemini-embedding-2",
                contents=batch
            )
            embedding_response.extend([e.values for e in response.embeddings])

            # Wait between batches
            if i + batch_size < len(text_chunks):
                time.sleep(delay)

        except Exception as ex:
            raise ex

    return embedding_response

def embed_text(text):
    response = client.models.embed_content(
        model="gemini-embedding-2",
        contents=[text]
    )
    return response.embeddings[0].values

def gemini_message(body: StreamRequestGemini) -> str:
    response = client.models.generate_content(
        model=body.model,
        contents=body.user_prompt,
        config={
            "temperature": body.temp,
            "max_output_tokens": 500
        }
    )

    return response.text