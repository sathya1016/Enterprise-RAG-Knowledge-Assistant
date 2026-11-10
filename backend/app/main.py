from fastapi import FastAPI

from app.api.documents import router as documents_router
from app.api.retrieval import router as retrieval_router
from app.api.answers import router as answers_router
from app.api.chat import router as chat_router
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True,
)
app = FastAPI(
    title="Enterprise RAG Knowledge Assistant",
    description="Enterprise document-based AI knowledge assistant",
    version="0.2.0"
)


@app.get("/")
async def root():

    return {
        "message": "Enterprise RAG Knowledge Assistant API",
        "status": "running"
    }


@app.get("/health")
async def health_check():

    return {
        "status": "healthy",
        "service": "rag-backend"
    }


@app.get("/api/v1/info")
async def application_info():

    return {
        "application": "Enterprise RAG Knowledge Assistant",
        "version": "0.2.0",
        "framework": "FastAPI"
    }


app.include_router(documents_router)

app.include_router(retrieval_router)

app.include_router(answers_router)

app.include_router(chat_router)