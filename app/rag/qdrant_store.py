from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.rag.config import (
    QDRANT_COLLECTION_NAME,
    QDRANT_HOST,
    QDRANT_PORT,
)


VECTOR_SIZE = 384


def get_qdrant_client() -> QdrantClient:
    return QdrantClient(
        host=QDRANT_HOST,
        port=QDRANT_PORT,
    )


def create_collection_if_not_exists() -> None:
    client = get_qdrant_client()

    collections = client.get_collections()

    existing_names = {
        collection.name
        for collection in collections.collections
    }

    if QDRANT_COLLECTION_NAME not in existing_names:
        client.create_collection(
            collection_name=QDRANT_COLLECTION_NAME,
            vectors_config=VectorParams(
                size=VECTOR_SIZE,
                distance=Distance.COSINE,
            ),
        )