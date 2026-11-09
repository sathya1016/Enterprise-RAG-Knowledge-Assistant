from pathlib import Path

from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

from app.core.config import settings


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