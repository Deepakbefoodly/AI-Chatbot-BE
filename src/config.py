import os

from dotenv import load_dotenv
from typing import Any
from pydantic_settings import BaseSettings

load_dotenv()

# Accessing secret keys and configs from env file
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
CHROMA_COLLECTION_NAME = os.getenv("CHROMA_COLLECTION_NAME")

class Config(BaseSettings):

    CORS_ORIGINS: list[str] = ["*"]
    CORS_HEADERS: list[str] = ["*"]
    APP_VERSION: str = "1"

settings = Config()

app_configs: dict[str, Any] = {
    "title": "React App - FastAPI Backend",
    "swagger_ui_parameters": {"displayRequestDuration": True},
}

openai_system_config: str = "You are a helpful assistant answering questions based on GitLab Handbook and Direction pages."