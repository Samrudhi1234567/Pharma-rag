from sentence_transformers import SentenceTransformer

from app.rag.config import EMBEDDING_MODEL


class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(EMBEDDING_MODEL)

    def embed_text(self, text: str) -> list[float]:
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        vector = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return vector.tolist()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        if not texts:
            return []

        vectors = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return vectors.tolist()