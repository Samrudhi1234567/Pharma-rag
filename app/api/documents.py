import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.auth.context import AuthorizationContext
from app.auth.dependencies import get_authorization_context
from app.ingestion.document_ingestion import ingest_document


router = APIRouter(
    prefix="/v1/documents",
    tags=["documents"],
)


class DocumentIngestRequest(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=500,
    )

    content: str = Field(
        min_length=1,
    )

    source: str | None = Field(
        default=None,
        max_length=1000,
    )

    content_type: str | None = Field(
        default="text/plain",
        max_length=100,
    )


class DocumentIngestResponse(BaseModel):
    document_id: str
    tenant_id: str
    owner_user_id: str
    status: str


@router.post(
    "/ingest",
    response_model=DocumentIngestResponse,
)
def ingest(
    request: DocumentIngestRequest,
    auth_context: AuthorizationContext = Depends(
        get_authorization_context
    ),
):
    tenant_id = uuid.UUID(auth_context.tenant_id)
    owner_user_id = uuid.UUID(auth_context.user_id)

    document_id = ingest_document(
        tenant_id=tenant_id,
        owner_user_id=owner_user_id,
        title=request.title,
        content=request.content,
        source=request.source,
        content_type=request.content_type,
    )

    return DocumentIngestResponse(
        document_id=str(document_id),
        tenant_id=str(tenant_id),
        owner_user_id=str(owner_user_id),
        status="completed",
    )