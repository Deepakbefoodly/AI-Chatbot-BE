from typing import Literal, List, Union

from pydantic import BaseModel

class MessageOpenAi(BaseModel):
    content: str
    role: Literal["system", "user", "assistant"]

class StreamRequestOpenAi(BaseModel):
    messages: List[MessageOpenAi]
    model: Literal["gpt-4", "gpt-3.5-turbo", "gpt-4o-mini"]
    temp: float

class StreamRequestGemini(BaseModel):
    user_prompt: str
    model: Literal["gemini-2.0-flash", "gemini-2.5-flash"]
    temp: float

class QuestionRequestGenAI(BaseModel):
    question: str
    llm: Literal["openai", "gemini"]
    model: Literal["gpt-4", "gpt-3.5-turbo", "gpt-4o-mini", "gemini-2.0-flash", "gemini-2.5-flash"]
    temp: float

class ResponseBody(BaseModel):
    answer: str
