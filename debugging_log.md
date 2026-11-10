# Enterprise RAG Knowledge Assistant — Debugging Log

## Project Overview

**Project:** Enterprise RAG Knowledge Assistant  
**Backend:** Python, FastAPI  
**Document Processing:** PyMuPDF  
**Text Splitting:** LangChain RecursiveCharacterTextSplitter  
**Embedding Provider:** OpenRouter  
**Embedding Model:** `openai/text-embedding-3-small`  
**Vector Database:** ChromaDB  
**Development Environment:** Windows, PowerShell, VS Code  
**Python Version:** 3.14  

This document records the errors encountered during project setup and implementation, their root causes, debugging approaches, resolutions, and validation results.

---

# 1. Project Setup — Stage 1

### Initial environment setup

**Activities completed:**
- Created GitHub repository.
- Cloned repository locally.
- Verified Python and Git installation.
- Created the local project workspace.
- Configured `.gitignore`.

No confirmed blocking errors were recorded during this stage.

---

# 2. Backend Foundation — Stage 2

### Activities completed

- Created Python virtual environment.
- Configured backend folder structure.
- Created FastAPI application.
- Implemented health-check endpoint.
- Implemented application information endpoint.
- Added initial API tests.
- Configured Git commits and GitHub push.

**Validation:**
- FastAPI application started successfully.
- Root endpoint returned HTTP 200.
- Health endpoint was implemented.
- Pytest was used to validate the initial API.

No specific Stage 2 application failure was recorded in the available debugging history.

---

# 3. PDF Document Ingestion — Stage 3

## Issue 1: Document upload returned HTTP 500

**Observed error:**

```json
{
  "detail": "Document ingestion failed"
}
```

**Root cause:**

The API returned a generic error response, which concealed the underlying exception occurring inside the document ingestion pipeline.

**Debugging approach:**

Added exception logging:

```python
logger.exception("Unexpected document ingestion error")
```

This allowed the complete Python traceback to be printed in the server console.

**Resolution:**

Improved exception handling and exposed the actual underlying failure through application logs.

**Lesson learned:**

Always inspect backend tracebacks instead of relying only on HTTP response codes.

---

## Issue 2: IndentationError in documents.py

**Observed error:**

```text
IndentationError: expected an indented block
after 'except' statement
```

**Root cause:**

The exception handler in `backend/app/api/documents.py` had incorrect indentation.

The logging statement was not properly placed inside the `except` block.

**Resolution:**

Replaced the entire `documents.py` implementation with correctly structured FastAPI endpoint code.

**Validation:**

```powershell
python -m py_compile backend/app/api/documents.py
```

No output indicated successful Python syntax validation.

**Lesson learned:**

Python indentation is part of the language syntax. Validate code after modifying exception-handling blocks.

---

## Issue 3: SyntaxError in documents.py

**Observed errors:**

```text
SyntaxError: expected 'except' or 'finally' block
```

```text
SyntaxError: invalid syntax
```

**Root cause:**

While modifying the exception handler, the `try` and `except` blocks became incorrectly structured.

Multiple edits introduced malformed exception-handling syntax.

**Resolution:**

Replaced the complete file instead of repeatedly modifying individual lines.

Validated the file using:

```powershell
python -m py_compile backend/app/api/documents.py
```

**Lesson learned:**

When a Python file has multiple syntax and indentation errors, replacing the affected function or file with a clean implementation is often safer than applying repeated small edits.

---

## Issue 4: Windows port conflict — Error 10048

**Observed error:**

```text
[Errno 10048] error while attempting to bind
on address ('127.0.0.1', 8000)

Only one usage of each socket address
is normally permitted.
```

**Root cause:**

Another Uvicorn process was already using port 8000.

Starting another server instance caused a port conflict.

**Debugging approach:**

Identified the process using:

```powershell
netstat -ano | findstr :8000
```

The final column provided the process ID.

**Resolution:**

Stopped the existing process:

```powershell
taskkill /PID <PID> /F
```

Restarted the FastAPI application.

**Lesson learned:**

Before starting a local development server, check whether the configured port is already occupied.

---

## Issue 5: OpenAI AuthenticationError — HTTP 401

**Observed error:**

```text
openai.AuthenticationError: Error code: 401

Incorrect API key provided: sk-or-v1...
```

**Root cause:**

The project used an OpenRouter API key but the LangChain OpenAI embedding client was configured to use the default OpenAI API endpoint.

The API key belonged to a different provider.

**Debugging approach:**

Inspected the traceback and identified the failure inside:

```text
langchain_openai/embeddings/base.py
```

The failure occurred during:

```python
embed_documents(texts)
```

**Resolution:**

Configured the OpenRouter API endpoint:

```env
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

Configured the embedding model:

```env
EMBEDDING_MODEL=openai/text-embedding-3-small
```

Updated the embedding client:

```python
self.embeddings = OpenAIEmbeddings(
    model=settings.EMBEDDING_MODEL,
    openai_api_key=settings.OPENAI_API_KEY,
    openai_api_base=settings.OPENAI_BASE_URL,
)
```

**Independent validation:**

Created a temporary API connection test.

Result:

```text
OpenRouter connection successful!
Model: text-embedding-3-small
Embedding dimensions: 1536
```

**Lesson learned:**

API authentication requires the correct provider endpoint, credentials, and supported model.

---

## Issue 6: ImportError — Settings object not found

**Observed error:**

```text
ImportError: cannot import name 'settings'
from 'app.core.config'
```

**Root cause:**

Some modules imported a global `settings` object:

```python
from app.core.config import settings
```

However, the configuration module initially exposed only the `get_settings()` function.

**Resolution:**

Added a global settings instance:

```python
@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
```

This maintained compatibility with the existing module imports.

**Validation:**

```powershell
python -c "from app.core.config import settings; print(settings.EMBEDDING_MODEL)"
```

Result:

```text
openai/text-embedding-3-small
```

**Lesson learned:**

Configuration interfaces must be consistent across application modules.

---

## Issue 7: AttributeError — chunk_size not found

**Observed error:**

```text
AttributeError:
'Settings' object has no attribute 'chunk_size'
```

**Root cause:**

The configuration class defined uppercase attributes:

```python
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
```

However, the text splitter referenced lowercase attributes:

```python
settings.chunk_size
settings.chunk_overlap
```

Pydantic settings attribute names are case-sensitive in this configuration.

**Resolution:**

Updated `backend/app/rag/text_splitter.py`:

```python
chunk_size=settings.CHUNK_SIZE,
chunk_overlap=settings.CHUNK_OVERLAP,
```

**Validation:**

```powershell
python -c "from app.rag.text_splitter import DocumentChunker; DocumentChunker(); print('Text splitter initialized successfully')"
```

Result:

```text
Text splitter initialized successfully
```

**Lesson learned:**

Maintain consistent naming conventions between configuration definitions and their usage.

---

## Issue 8: PyMuPDF deprecation warning

**Observed warning:**

```text
FutureWarning: The fitz API is deprecated.
Use import pymupdf instead.
```

**Root cause:**

The PDF loader used the older `fitz` import interface.

**Resolution:**

Replaced:

```python
import fitz
```

With:

```python
import pymupdf
```

Also replaced:

```python
fitz.open(...)
```

With:

```python
pymupdf.open(...)
```

**Lesson learned:**

Prefer supported library interfaces and address deprecation warnings before they become compatibility problems.

---

# 4. Integration Validation

After resolving the above issues, the following validation checks were completed.

### Configuration validation

```powershell
python -c "from app.core.config import settings; print('Config loaded:', settings.EMBEDDING_MODEL)"
```

Result: Successful.

### Application import validation

```powershell
python -c "from app.main import app; print('FastAPI application imported successfully')"
```

Result:

```text
FastAPI application imported successfully
```

### Text splitter validation

Result:

```text
Text splitter initialized successfully
```

### Vector store validation

Result:

```text
Vector store initialized successfully
```

### FastAPI server validation

```powershell
python -m uvicorn app.main:app --app-dir backend --log-level debug
```

Result:

```text
Application startup complete.
Uvicorn running on http://127.0.0.1:8000
```

---

# 5. Final PDF Ingestion Test

**Test document:** UserManual_JointDeclaration_member.pdf

**API endpoint:**

```http
POST /api/v1/documents/upload
```

**Final response:**

```json
{
  "document_id": "4300604d-4d74-4bd0-9121-aff54ac1673a",
  "filename": "UserManual_JointDeclaration_member.pdf",
  "pages_processed": 20,
  "chunks_created": 27,
  "vectors_stored": 27,
  "status": "completed"
}
```

**Final result:**

- HTTP response: 200 OK
- Pages processed: 20
- Chunks generated: 27
- Embeddings generated: 27
- Vectors stored: 27
- Document ingestion status: completed

Stage 3 document ingestion was successfully validated.

---

# 6. Reverse Engineering and Debugging Methodology

The following systematic approach was used throughout debugging.

1. **Observe:** Identify the error from the API response, terminal, or application logs.
2. **Reproduce:** Repeat the operation to confirm that the issue is consistent.
3. **Trace:** Follow the traceback to the responsible file, function, and line.
4. **Identify:** Determine the underlying technical cause.
5. **Resolve:** Apply the smallest appropriate code or configuration change.
6. **Validate:** Test the affected component independently.
7. **Integrate:** Run the complete workflow again to confirm the fix.

### Key engineering practices learned

- Exception handling and structured application logging.
- Python syntax and indentation validation.
- Windows process and port management.
- Third-party API authentication and endpoint configuration.
- Environment-based application configuration.
- Pydantic settings management.
- LangChain embedding integration.
- PDF text extraction and document chunking.
- Vector database initialization and persistence.
- Independent component testing and end-to-end validation.

---

# 7. Current Project Status

| Stage | Description | Status |
|---|---|---|
| Stage 1 | Repository and environment setup | Completed |
| Stage 2 | FastAPI backend foundation | Completed |
| Stage 3 | PDF ingestion and vector storage | Completed |
| Stage 4 | Semantic retrieval | Pending |
| Stage 5 | LLM answer generation | Pending |
| Stage 6 | RAG chat API and citations | Pending |
| Stage 7 | Testing and RAG evaluation | Pending |
| Stage 8 | Production readiness and deployment | Pending |

**Note:** This log records the errors and fixes confirmed during development. No additional failures are assumed where the available logs did not establish them.


## Stage 4 – Retrieval Performance Investigation

### Problem
The semantic retrieval API initially took approximately 43–45 seconds to process a query.

### Investigation and debugging steps

1. Added timing measurements to identify the slow component.
2. Separated embedding API execution time from ChromaDB search time.
3. Tested OpenRouter embeddings using the direct OpenAI SDK.
4. Tested embeddings independently using LangChain.
5. Verified that RetrievalService and VectorStore instances were reused across API requests.
6. Inspected HTTP client configuration, timeout and retry settings.
7. Compared standalone embedding execution with embedding execution through FastAPI.
8. Verified Python executable, process ID, embedding model and API base URL.

### Code changes

**File: backend/app/api/retrieval.py**
- Moved RetrievalService initialization outside the endpoint.
- Reused the same service instance across requests.

**File: backend/app/rag/vector_store.py**
- Added explicit embedding request timeout of 15 seconds.
- Configured maximum retries to 1.
- Separated query embedding generation from ChromaDB search.
- Added individual performance measurements for embedding generation and vector search.

### Performance results

| Measurement | Earlier result | Latest result |
|---|---:|---:|
| Embedding generation | ~43 seconds | 0.572–1.174 seconds |
| ChromaDB search | 0.007–0.285 seconds | 0.003–0.086 seconds |
| Total retrieval | ~43–45 seconds | 0.576–1.260 seconds |

### Outcome
The latest FastAPI tests completed retrieval in approximately 1 second.

The original delay was intermittent. Its exact root cause was not conclusively established.

### Technical learning
- Profile individual components before optimizing.
- Separate remote API latency from local vector database latency.
- Reuse service and client instances.
- Measure performance inside the actual application execution path.
- Avoid assuming that a successful HTTP response means the request was fast.