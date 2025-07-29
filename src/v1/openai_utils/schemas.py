from typing import Literal, List

from pydantic import BaseModel

class MessageOpenAi(BaseModel):
    content: str
    role: Literal["system", "user", "assistant"]

class StreamRequestOpenAi(BaseModel):
    messages: List[MessageOpenAi]
    model: Literal["gpt-4", "gpt-3.5-turbo", "gpt-4o-mini"]
    temp: float

class QuestionRequestGenAI(BaseModel):
    question: str
    model: Literal["gpt-4", "gpt-3.5-turbo", "gpt-4o-mini"]
    temp: float
