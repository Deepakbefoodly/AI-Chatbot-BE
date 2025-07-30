import google.generativeai as genai
import time
from src.config import GEMINI_API_KEY
from src.v1.schemas import StreamRequestGemini

genai.configure(api_key=GEMINI_API_KEY)

batch_size: int = 50
delay: float = 1.0

def generate_embeddings(text_chunks):
    embedding_response = []
    model = genai.embed_content

    try:
        # embedding in batches to avoid rate limit error
        for i in range(0, len(text_chunks), batch_size):
            batch = text_chunks[i:i + batch_size]

            for chunk in batch:
                if not chunk.strip():
                    continue

                response = model(
                    model="models/embedding-001",
                    content=chunk,
                    task_type="retrieval_document"
                )
                embedding_response.append(response["embedding"])

            # Wait between batches
            if i + batch_size < len(text_chunks):
                time.sleep(delay)

    except Exception as ex:
        raise ex

    return embedding_response

def embed_text(text):
    model = genai.embed_content
    return model(model="models/embedding-001", content=text, task_type="retrieval_document")["embedding"]

def gemini_message(body: StreamRequestGemini) -> str:
    model = genai.GenerativeModel(
        model_name=body.model,
        generation_config={
            "temperature": body.temp,
            "max_output_tokens": 500
        })

    # Initialize Gemini chat model
    chat = model.start_chat(history=[
        {"role": "model", "parts": [body.system_prompt]}
    ])

    # Ask a new question
    response = chat.send_message(body.user_prompt)

    return response.text