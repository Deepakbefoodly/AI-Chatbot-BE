from typing import List

from src.config import OPENAI_API_KEY
import time

from openai import OpenAI, AsyncOpenAI, RateLimitError
from src.v1.schemas import MessageOpenAi, StreamRequestOpenAi

client = OpenAI(api_key=OPENAI_API_KEY)
asyncClient = AsyncOpenAI(api_key=OPENAI_API_KEY)

batch_size: int = 5
delay: float = 1.0

def create_prompt_message(related_content: List[str], user_question: str) -> MessageOpenAi:
    context = "\n\n".join(related_content)
    prompt = f"""
        You are an expert AI assistant trained on the GitLab Handbook and Github Direction data set.
        
        Answer the user's question based **only on the context provided below**.
        If the answer is not found in the context, reply with "I couldn't find that information in the provided data."
        
        ### CONTEXT:
        {context}
        
        ### QUESTION:
        {user_question}
        
        ### INSTRUCTIONS:
        - Be concise and factual.
        - Don’t hallucinate or make assumptions.
        - If the context is not relevant, say so clearly.
        """

    user_message = MessageOpenAi(
        role="user",
        content=prompt.strip()
    )

    return user_message

async def openai_message(body: StreamRequestOpenAi) -> str:

    # Convert custom Pydantic message objects to dicts
    messages = [{"role": msg.role, "content": msg.content} for msg in body.messages]

    # Begin a task to run in the background
    response = await asyncClient.chat.completions.create(
        model=body.model,
        messages=messages,
        temperature=body.temp
    )
    return response.choices[0].message.content.strip()

def generate_embeddings(text_chunks):
    embedding_response = []

    # embedding in batches to avoid rate limit error
    for i in range(0, len(text_chunks), batch_size):
        batch = text_chunks[i:i + batch_size]

        try:
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )

            batch_embeddings = [emb.embedding for emb in response.data]
            embedding_response.extend(batch_embeddings)

            # Wait between batches
            if i + batch_size < len(text_chunks):
                time.sleep(delay)

        except RateLimitError:
            time.sleep(60)  # Wait 1 minute
            # Retry this batch
            response = client.embeddings.create(
                model="text-embedding-3-small",
                input=batch
            )
            batch_embeddings = [emb.embedding for emb in response.data]
            embedding_response.extend(batch_embeddings)

    return embedding_response

def embed_text(text):
    return client.embeddings.create(input=[text], model="text-embedding-3-small").data[0].embedding
