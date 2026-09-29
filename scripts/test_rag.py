import uuid

from app.rag.rag_service import RAGService


TENANT_ID = uuid.UUID(
    "f46efbed-bbdb-4d08-b312-bdd8263ac1fd"
)


service = RAGService()

response = service.query(
    query="What is paracetamol used for?",
    tenant_id=TENANT_ID,
    limit=5,
)

print("Answer:")
print(response.answer)

print()
print("Sources:", len(response.sources))

for source in response.sources:
    print("---")
    print("Document:", source.document_id)
    print("Tenant:", source.tenant_id)
    print("Chunk:", source.chunk_index)
    print("Score:", source.score)