
from app.rag.vector_store import VectorStore


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

        results = self.vector_store.similarity_search(
            query=query.strip(),
            document_id=document_id,
            k=top_k,
        )

        return {
            "query": query,
            "document_id": document_id,
            "total_results": len(results),
            "results": results,
        }