import uuid

from app.rag.retrieval_service import retrieve_context


TENANT_ID = uuid.UUID(
    "f46efbed-bbdb-4d08-b312-bdd8263ac1fd"
)


results = retrieve_context(
    query="What is paracetamol used for?",
    tenant_id=TENANT_ID,
    limit=5,
)

print("Retrieved chunks:", len(results))

for result in results:
    print("---")
    print("Document:", result.document_id)
    print("Tenant:", result.tenant_id)
    print("Chunk:", result.chunk_index)
    print("Score:", result.score)
    print("Content:", result.content)