from app.rag.embeddings import EmbeddingService


_embedding_service = EmbeddingService()


def embed_text(text: str) -> list[float]:
    """Generate a single embedding using the shared embedding service."""
    return _embedding_service.embed_text(text)


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Generate multiple embeddings using the shared embedding service."""
    return _embedding_service.embed_documents(texts)