import uuid
from dataclasses import dataclass

from app.rag.llm import LLMService
from app.rag.retrieval_service import RetrievedChunk, retrieve_context


@dataclass
class RAGResponse:
    answer: str
    sources: list[RetrievedChunk]


class RAGService:
    def __init__(self):
        self.llm = LLMService()

    def query(
        self,
        *,
        query: str,
        tenant_id: uuid.UUID,
        limit: int = 5,
    ) -> RAGResponse:
        if not query or not query.strip():
            raise ValueError("Query cannot be empty")

        retrieved_chunks = retrieve_context(
            query=query,
            tenant_id=tenant_id,
            limit=limit,
        )

        if not retrieved_chunks:
            return RAGResponse(
                answer="I could not find any authorized information "
                "relevant to your question.",
                sources=[],
            )

        context = "\n\n".join(
            (
                f"[Source {index + 1}]\n"
                f"Document ID: {chunk.document_id}\n"
                f"Chunk: {chunk.chunk_index}\n"
                f"Content: {chunk.content}"
            )
            for index, chunk in enumerate(retrieved_chunks)
        )

        answer = self.llm.generate(
            query=query,
            context=context,
        )

        return RAGResponse(
            answer=answer,
            sources=retrieved_chunks,
        )