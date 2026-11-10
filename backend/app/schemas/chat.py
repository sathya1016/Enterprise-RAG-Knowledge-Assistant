
from typing import Literal

from pydantic import BaseModel, Field

from app.schemas.answer import AnswerSource


class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=4000)


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    document_id: str = Field(min_length=1)
    top_k: int = Field(default=4, ge=1, le=10)

    # Recent conversation messages supplied by the client.
    history: list[ChatMessage] = Field(
        default_factory=list,
        max_length=10,
    )


class ChatResponse(BaseModel):
    message: str
    document_id: str
    answer: str
    total_sources: int
    sources: list[AnswerSource]
 