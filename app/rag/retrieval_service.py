import uuid
from dataclasses import dataclass

from sqlalchemy import select

from app.db.models import DocumentChunk
from app.db.session import SessionLocal
from app.rag.retriever import search_documents


@dataclass
class RetrievedChunk:
    document_id: str
    tenant_id: str
    chunk_index: int
    content: str
    score: float


def retrieve_context(
    *,
    query: str,
    tenant_id: uuid.UUID,
    limit: int = 5,
) -> list[RetrievedChunk]:
    """
    Retrieve authorized document chunks.

    Qdrant performs semantic retrieval with the tenant filter.
    PostgreSQL provides the authoritative chunk content.
    """

    results = search_documents(
        query=query,
        tenant_id=tenant_id,
        limit=limit,
    )

    if not results:
        return []

    db = SessionLocal()

    try:
        retrieved_chunks = []

        for result in results:
            payload = result.payload or {}

            document_id = uuid.UUID(str(payload["document_id"]))
            chunk_index = int(payload["chunk_index"])

            statement = select(DocumentChunk).where(
                DocumentChunk.document_id == document_id,
                DocumentChunk.chunk_index == chunk_index,
                DocumentChunk.tenant_id == tenant_id,
            )

            chunk = db.execute(statement).scalar_one_or_none()

            if chunk is None:
                continue

            retrieved_chunks.append(
                RetrievedChunk(
                    document_id=str(chunk.document_id),
                    tenant_id=str(chunk.tenant_id),
                    chunk_index=chunk.chunk_index,
                    content=chunk.content,
                    score=float(result.score),
                )
            )

        return retrieved_chunks

    finally:
        db.close()