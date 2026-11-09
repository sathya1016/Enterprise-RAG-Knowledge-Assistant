from fastapi import FastAPI
from datetime import datetime, timezone

app = FastAPI(
    title="Enterprise RAG Knowledge Assistant",
    description="An enterprise document-based AI knowledge assistant",
    version="0.1.0"
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
        "service": "rag-backend",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@app.get("/api/v1/info")
async def application_info():
    return {
        "application": "Enterprise RAG Knowledge Assistant",
        "version": "0.1.0",
        "framework": "FastAPI",
        "status": "development"
    }