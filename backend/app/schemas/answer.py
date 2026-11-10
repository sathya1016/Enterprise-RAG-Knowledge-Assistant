from typing import Optional

from pydantic import BaseModel, Field


class AnswerRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=2000,
        description="Question asked about the uploaded document",
    )

    document_id: str = Field(
        min_length=1,
        description="ID of the uploaded document",
    )

    top_k: int = Field(
        default=4,
        ge=1,
        le=10,
        description="Number of relevant chunks to retrieve",
    )


class AnswerSource(BaseModel):
    filename: Optional[str] = None
    page: Optional[int] = None
    chunk_index: Optional[int] = None
    distance: Optional[float] = None


class AnswerResponse(BaseModel):
    query: str
    document_id: str
    answer: str
    total_sources: int
    sources: list[AnswerSource]