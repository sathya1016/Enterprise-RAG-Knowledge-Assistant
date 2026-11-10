
import logging

from fastapi import APIRouter, HTTPException
from starlette.concurrency import run_in_threadpool

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat import chat_service


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
async def chat_with_document(request: ChatRequest):
    try:
        result = await run_in_threadpool(
            chat_service.chat,
            message=request.message,
            document_id=request.document_id,
            top_k=request.top_k,
            history=[
                item.model_dump()
                for item in request.history
            ],
        )

        return result

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc),
        ) from exc

    except Exception:
        logger.exception("Chat API request failed")

        raise HTTPException(
            status_code=502,
            detail="Chat request failed. Check server logs.",
        )
