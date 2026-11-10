import os
import sys
import logging

from fastapi import APIRouter, HTTPException

from app.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
)
from app.services.retrieval import RetrievalService
retrieval_service = RetrievalService()
import time
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/retrieval",
    tags=["Retrieval"],
)



@router.post("/search", response_model=RetrievalResponse)
async def search_documents(request: RetrievalRequest):
    
    
    start_time = time.perf_counter()
    try:
        service = retrieval_service

        result = service.retrieve(
            query=request.query,
            document_id=request.document_id,
            top_k=request.top_k,
        )
        
     
        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception("Document retrieval failed")

        raise HTTPException(
            status_code=500,
            detail="Document retrieval failed. Check server logs.",
        )
