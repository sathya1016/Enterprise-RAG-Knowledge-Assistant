
from app.rag.vector_store import VectorStore

from app.core.config import settings
class RetrievalService:

    def __init__(self):
        self.vector_store = VectorStore()



    def retrieve(
        self,
        query: str,
        document_id: str,
        top_k: int = 4,
    ):
        if not query or not query.strip():
            raise ValueError("Question cannot be empty")

        if not document_id:
            raise ValueError("Document ID is required")

    # Step 1: Retrieve candidate chunks
        retrieved_results = self.vector_store.similarity_search(
            query=query.strip(),
            document_id=document_id,
            k=top_k,
        )

    # Step 2: Filter chunks using distance threshold
        threshold = settings.RETRIEVAL_DISTANCE_THRESHOLD

        relevant_results = [
            result
            for result in retrieved_results
            if result["distance"] <= threshold
        ]

        return {
            "query": query,
            "document_id": document_id,
            "total_results": len(relevant_results),
            "results": relevant_results,
        }
# Shared retrieval service instance
retrieval_service = RetrievalService()