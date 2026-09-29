import uuid

from app.db.models import Document, DocumentChunk
from app.db.session import SessionLocal
from app.ingestion.chunker import chunk_text
from app.ingestion.embedder import embed_texts
from app.rag.qdrant_store import get_qdrant_client
from app.rag.config import QDRANT_COLLECTION_NAME


def ingest_document(
    *,
    tenant_id: uuid.UUID,
    title: str,
    content: str,
    source: str | None = None,
    content_type: str | None = "text/plain",
    owner_user_id: uuid.UUID | None = None,
) -> uuid.UUID:
    """
    Ingest a document into PostgreSQL and Qdrant.

    Flow:
        text -> chunks -> embeddings -> PostgreSQL + Qdrant
    """

    if not content.strip():
        raise ValueError("Document content cannot be empty")

    chunks = chunk_text(content)

    if not chunks:
        raise ValueError("No chunks were generated from document")

    db = SessionLocal()

    try:
        # 1. Create document record
        document = Document(
            tenant_id=tenant_id,
            owner_user_id=owner_user_id,
            title=title,
            source=source,
            content_type=content_type,
            status="processing",
        )

        db.add(document)
        db.flush()

        # 2. Generate embeddings for all chunks
        chunk_contents = [chunk.content for chunk in chunks]
        embeddings = embed_texts(chunk_contents)

        if len(embeddings) != len(chunks):
            raise RuntimeError("Embedding count does not match chunk count")

        qdrant = get_qdrant_client()

        # 3. Prepare Qdrant points
        points = []

        document_chunks = []

        for chunk, embedding in zip(chunks, embeddings):
            point_id = uuid.uuid4()

            document_chunk = DocumentChunk(
                document_id=document.id,
                tenant_id=tenant_id,
                chunk_index=chunk.chunk_index,
                content=chunk.content,
                qdrant_point_id=point_id,
            )

            document_chunks.append(document_chunk)

            points.append(
                {
                    "id": point_id,
                    "vector": embedding,
                    "payload": {
                        "document_id": str(document.id),
                        "tenant_id": str(tenant_id),
                        "owner_user_id": (
                            str(owner_user_id)
                            if owner_user_id
                            else None
                        ),
                        "chunk_index": chunk.chunk_index,
                    },
                }
            )

        # 4. Insert chunks into PostgreSQL
        db.add_all(document_chunks)

        # 5. Insert vectors into Qdrant
        qdrant.upsert(
            collection_name=QDRANT_COLLECTION_NAME,
            points=points,
        )

        # 6. Mark document as completed
        document.status = "completed"

        db.commit()

        return document.id

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()