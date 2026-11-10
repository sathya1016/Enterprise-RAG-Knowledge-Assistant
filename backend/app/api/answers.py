import logging

from fastapi import APIRouter, HTTPException

from app.schemas.answer import (
    AnswerRequest,
    AnswerResponse,
)

from app.services.answer_generation import (
    answer_generation_service,
)


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/answers",
    tags=["Answers"],
)


@router.post(
    "/generate",
    response_model=AnswerResponse,
)
async def generate_document_answer(
    request: AnswerRequest,
):

    try:

        result = answer_generation_service.generate_answer(
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

        logger.exception(
            "Answer generation failed"
        )

        raise HTTPException(
            status_code=502,
            detail=(
                "Answer generation failed. "
                "Check server logs."
            ),
        )