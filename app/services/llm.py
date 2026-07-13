from langchain_mistralai import ChatMistralAI
from app.config import settings

llm=ChatMistralAI(
    model=settings.MODEL_NAME,
    api_key=settings.MISTRAL_API_KEY,
    temperature=0.2
)