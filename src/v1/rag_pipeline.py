from config import openai_system_config

# from openai_utils.service import embed_text
from openai_utils.service import create_prompt_message, openai_message
from gemini_utils.service import embed_text, gemini_message
from vector_store import query_similar_docs
from v1.schemas import QuestionRequestGenAI, MessageOpenAi, StreamRequestOpenAi, StreamRequestGemini

def run_rag_pipeline(body: QuestionRequestGenAI):
    embedding = embed_text(body.question)
    relevant_data = query_similar_docs(embedding)

    user_message: MessageOpenAi = create_prompt_message(relevant_data, body.question)
    system_message: MessageOpenAi = MessageOpenAi(
        role="system",
        content= openai_system_config
    )

    message_list = [system_message, user_message]

    if body.llm == "openai":
        llm_body = StreamRequestOpenAi(
            messages=message_list,
            model=body.model,
            temp=body.temp
        )
        return openai_message(llm_body)
    else:
        llm_body = StreamRequestGemini(
            user_prompt=user_message.content,
            system_prompt=system_message.content,
            model=body.model,
            temp=body.temp
        )
        return gemini_message(llm_body)