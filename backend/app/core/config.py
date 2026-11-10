from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"

    EMBEDDING_MODEL: str = "text-embedding-3-small"

    CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200

    CHROMA_PERSIST_DIRECTORY: str = "./data/chroma"
    CHROMA_COLLECTION_NAME: str = "enterprise_documents"

    MAX_UPLOAD_SIZE_MB: int = 10
    CHAT_MODEL: str = "openai/gpt-4o-mini"
    RETRIEVAL_DISTANCE_THRESHOLD: float = 1.5
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()