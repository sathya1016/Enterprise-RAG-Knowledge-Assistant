import pymupdf

from langchain_core.documents import Document


class PDFLoader:

    @staticmethod
    def load_pdf(file_content: bytes, filename: str) -> list[Document]:

        if not file_content.startswith(b"%PDF-"):
            raise ValueError("Invalid PDF file")

        documents = []

        try:
            with pymupdf.open(
                stream=file_content,
                filetype="pdf"
            ) as pdf:

                if pdf.needs_pass:
                    raise ValueError(
                        "Password-protected PDFs are not supported"
                    )

                for page_number, page in enumerate(pdf, start=1):

                    text = page.get_text("text").strip()

                    if not text:
                        continue

                    documents.append(
                        Document(
                            page_content=text,
                            metadata={
                                "source": filename,
                                "page": page_number
                            }
                        )
                    )

        except ValueError:
            raise

        except Exception as exc:
            raise ValueError(
                "Unable to extract text from PDF"
            ) from exc

        if not documents:
            raise ValueError(
                "No extractable text found in PDF"
            )

        return documents