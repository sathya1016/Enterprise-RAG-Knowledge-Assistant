from uuid import uuid4

from app.rag.pdf_loader import PDFLoader
from app.rag.text_splitter import DocumentChunker
from app.rag.vector_store import VectorStore


class IngestionService:

    def __init__(self):

        self.pdf_loader = PDFLoader()
        self.chunker = DocumentChunker()
        self.vector_store = VectorStore()

    def ingest_pdf(
        self,
        file_content: bytes,
        filename: str
    ):

        document_id = str(uuid4())

        # Step 1: Extract PDF text
        documents = self.pdf_loader.load_pdf(
            file_content,
            filename
        )

        # Step 2: Split into chunks
        chunks = self.chunker.split_documents(
            documents,
            document_id
        )

        # Step 3: Generate embeddings and store vectors
        vector_ids = self.vector_store.add_documents(
            chunks,
            document_id
        )

        return {
            "document_id": document_id,
            "filename": filename,
            "pages_processed": len(documents),
            "chunks_created": len(chunks),
            "vectors_stored": len(vector_ids),
            "status": "completed"
        }