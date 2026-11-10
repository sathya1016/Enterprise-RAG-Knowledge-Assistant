
from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=2000,
        description="Question to search in the uploaded document",
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


class RetrievedChunk(BaseModel):
    content: str
    metadata: dict
    distance: float


class RetrievalResponse(BaseModel):
    query: str
    document_id: str
    total_results: int
    results: list[RetrievedChunk]
