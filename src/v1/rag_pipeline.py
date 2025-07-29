from config import openai_system_config

from openai_utils.service import embed_text, create_openai_message, send_message
from vector_store import query_similar_docs
from openai_utils.schemas import QuestionRequestGenAI, MessageOpenAi, StreamRequestOpenAi

def run_rag_pipeline(body: QuestionRequestGenAI):
    embedding = embed_text(body.question)
    relevant_data = query_similar_docs(embedding)

    user_message: MessageOpenAi = create_openai_message(relevant_data, body.question)
    system_message: MessageOpenAi = MessageOpenAi(
        role="system",
        content= openai_system_config
    )

    message_list = [system_message, user_message]

    openai_body = StreamRequestOpenAi(
        messages=message_list,
        model=body.model,
        temp=body.temp
    )

    return send_message(openai_body)


