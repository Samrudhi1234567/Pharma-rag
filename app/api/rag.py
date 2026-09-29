import uuid

from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field

from app.auth.context import AuthorizationContext
from app.auth.dependencies import get_authorization_context
from app.rag.rag_service import RAGService


router = APIRouter(
    prefix="/v1/rag",
    tags=["rag"],
)

rag_service = RAGService()


class RAGQueryRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=2000,
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
    )


class RAGSource(BaseModel):
    document_id: str
    tenant_id: str
    chunk_index: int
    score: float


class RAGQueryResponse(BaseModel):
    trace_id: str
    answer: str
    sources: list[RAGSource]


@router.post(
    "/query",
    response_model=RAGQueryResponse,
)
def query_rag(
    request: RAGQueryRequest,
    auth_context: AuthorizationContext = Depends(
        get_authorization_context
    ),
):
    trace_id = str(uuid.uuid4())

    tenant_id = uuid.UUID(auth_context.tenant_id)

    result = rag_service.query(
        query=request.query,
        tenant_id=tenant_id,
        limit=request.limit,
    )

    return RAGQueryResponse(
        trace_id=trace_id,
        answer=result.answer,
        sources=[
            RAGSource(
                document_id=source.document_id,
                tenant_id=source.tenant_id,
                chunk_index=source.chunk_index,
                score=source.score,
            )
            for source in result.sources
        ],
    )
