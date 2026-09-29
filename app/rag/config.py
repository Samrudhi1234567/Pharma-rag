import os


QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", "6333"))

QDRANT_COLLECTION_NAME = os.getenv(
    "QDRANT_COLLECTION_NAME",
    "pharma_documents",
)

EMBEDDING_PROVIDER = os.getenv(
    "EMBEDDING_PROVIDER",
    "huggingface",
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "sentence-transformers/all-MiniLM-L6-v2",
)

EMBEDDING_DIMENSION = 384

LLM_PROVIDER = os.getenv(
    "LLM_PROVIDER",
    "mock",
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "mock-rag",
)