from qdrant_client.models import PayloadSchemaType

from app.rag.qdrant_store import get_qdrant_client
from app.rag.config import QDRANT_COLLECTION_NAME


def create_payload_indexes() -> None:
    client = get_qdrant_client()

    fields = {
        "tenant_id": PayloadSchemaType.KEYWORD,
        "document_id": PayloadSchemaType.KEYWORD,
        "owner_user_id": PayloadSchemaType.KEYWORD,
    }

    for field_name, field_schema in fields.items():
        client.create_payload_index(
            collection_name=QDRANT_COLLECTION_NAME,
            field_name=field_name,
            field_schema=field_schema,
        )