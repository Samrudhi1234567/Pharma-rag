import uuid

from qdrant_client.models import (
    FieldCondition,
    Filter,
    MatchValue,
)

from app.rag.config import QDRANT_COLLECTION_NAME
from app.rag.embeddings import EmbeddingService
from app.rag.qdrant_store import get_qdrant_client


embedding_service = EmbeddingService()


def search_documents(
    *,
    query: str,
    tenant_id: uuid.UUID,
    limit: int = 5,
):
    """
    Search Qdrant for relevant document chunks.

    tenant_id is supplied by the trusted server-side
    authorization context and is always applied to the
    Qdrant search filter.
    """

    if not query or not query.strip():
        raise ValueError("Query cannot be empty")

    if limit <= 0:
        raise ValueError("limit must be greater than 0")

    query_vector = embedding_service.embed_text(query)

    tenant_filter = Filter(
        must=[
            FieldCondition(
                key="tenant_id",
                match=MatchValue(
                    value=str(tenant_id),
                ),
            )
        ]
    )

    client = get_qdrant_client()

    results = client.query_points(
        collection_name=QDRANT_COLLECTION_NAME,
        query=query_vector,
        query_filter=tenant_filter,
        limit=limit,
        with_payload=True,
    )

    return results.points