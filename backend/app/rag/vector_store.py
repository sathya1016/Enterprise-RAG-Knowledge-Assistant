from pathlib import Path

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings
import logging
import time
import httpx

logger = logging.getLogger(__name__)

class VectorStore:

    def __init__(self):

        persist_directory = Path(
            settings.CHROMA_PERSIST_DIRECTORY
        )

        persist_directory.mkdir(
            parents=True,
            exist_ok=True
        )

        self.embeddings = OpenAIEmbeddings(
            model=settings.EMBEDDING_MODEL,
            openai_api_key=settings.OPENAI_API_KEY,
            openai_api_base=settings.OPENAI_BASE_URL,
            timeout=15.0,
            max_retries=1,
        )

        


        self.vector_db = Chroma(
            collection_name=settings.CHROMA_COLLECTION_NAME,
            embedding_function=self.embeddings,
            persist_directory=str(persist_directory)
        )


    def add_documents(self, chunks, document_id):

        ids = [
            f"{document_id}_{chunk.metadata['chunk_index']}"
            for chunk in chunks
        ]

        self.vector_db.add_documents(
            documents=chunks,
            ids=ids
        )

        return ids

    def search(self, query: str, k: int = 5):

        return self.vector_db.similarity_search(
            query,
            k=k
        )


    def similarity_search(self, query: str, document_id: str, k: int = 4):
    # Step 1: Generate query embedding
        embedding_start = time.perf_counter()
    
        query_embedding = self.embeddings.embed_query(query)

        embedding_time = time.perf_counter() - embedding_start
        

    # Step 2: Search ChromaDB using the generated embedding
        search_start = time.perf_counter()

        results = self.vector_db._collection.query(
            query_embeddings=[query_embedding],
            n_results=k,
            where={"document_id": document_id},
            include=["documents", "metadatas", "distances"],
        )

        search_time = time.perf_counter() - search_start

    # Step 3: Format results
        formatted_results = []

        for index in range(len(results["documents"][0])):
            formatted_results.append({
                "content": results["documents"][0][index],
                "metadata": results["metadatas"][0][index],
                "distance": float(results["distances"][0][index]),
            })

        return formatted_results
