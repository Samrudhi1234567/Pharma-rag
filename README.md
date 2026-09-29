# Pharma Production RAG

A production-oriented Retrieval-Augmented Generation (RAG) API for secure pharmaceutical information retrieval using FastAPI, PostgreSQL, Qdrant, Redis, Keycloak, MLflow and Hugging Face LLMs.

## Project Overview

This project implements a containerized Pharma RAG application designed around secure, tenant-aware retrieval of pharmaceutical information.

The application provides an authenticated API workflow where:

1. A user authenticates through Keycloak.
2. The authenticated user's tenant context is extracted server-side from the JWT.
3. The tenant context is used to restrict vector retrieval.
4. Relevant document chunks are retrieved from Qdrant.
5. Authoritative document content is retrieved from PostgreSQL.
6. Retrieved context is provided to the LLM.
7. The LLM generates a grounded response based on the available information.
8. The API returns the generated answer together with source information and a unique trace ID.

## Key Features Implemented

### 1. Containerized Application Architecture

The complete application stack is containerized using Docker Compose.

The current stack includes:

* **FastAPI** – RAG API
* **PostgreSQL** – relational database and authoritative document storage
* **Qdrant** – vector database for semantic retrieval
* **Redis** – application infrastructure
* **Keycloak** – authentication and authorization infrastructure
* **MLflow** – ML lifecycle and evaluation infrastructure
* **Hugging Face** – LLM inference

All core services are running successfully in the local Docker environment.

### 2. Keycloak Authentication

Keycloak is integrated with the Pharma RAG API for authentication.

The API requires a valid Bearer access token for protected RAG requests.

The authenticated JWT is validated by the API before processing the request.

The application extracts the authenticated user's tenant information from the server-side authorization context.

### 3. Server-Side Tenant Isolation

Tenant information is not accepted as a client-controlled parameter in the RAG request.

Instead, the tenant is derived from the authenticated user's Keycloak token.

The tenant ID is then applied as a server-side filter during Qdrant retrieval.

This ensures that semantic retrieval is restricted to documents belonging to the authenticated tenant.

### 4. Vector Retrieval with Qdrant

Qdrant is used as the vector database for semantic document retrieval.

The application:

* Generates an embedding for the user query.
* Applies the authenticated tenant filter.
* Retrieves relevant document chunks.
* Returns document identifiers, chunk information and similarity scores.

The retrieved chunks are subsequently validated against PostgreSQL before being used as RAG context.

### 5. PostgreSQL as Authoritative Storage

PostgreSQL stores the authoritative document and document-chunk information.

After Qdrant retrieval, the application retrieves the corresponding document content from PostgreSQL.

The PostgreSQL lookup also validates the tenant ID, providing an additional server-side consistency check.

### 6. Hugging Face LLM Integration

The application integrates a Hugging Face-hosted instruction-tuned LLM for response generation.

The retrieved document context is supplied to the LLM through a grounded RAG prompt.

The system is designed to generate answers using the retrieved pharmaceutical information rather than relying only on unsupported model knowledge.

### 7. Trace ID

Each RAG request receives a unique `trace_id`.

The trace ID is returned in the API response and can be used to identify an individual RAG request during debugging, testing and future observability integration.

### 8. Health and Readiness Monitoring

The application provides:

* `/healthz` – basic application health check
* `/readyz` – dependency readiness check

The readiness endpoint currently verifies connectivity with:

* PostgreSQL
* Qdrant
* Redis
* MLflow
* Keycloak

All five dependencies have been successfully verified as healthy in the current deployment.

## Architecture

```text
                         +----------------+
                         |     Client     |
                         +-------+--------+
                                 |
                                 | Bearer Token
                                 v
                         +----------------+
                         |   FastAPI RAG  |
                         |      API      |
                         +-------+--------+
                                 |
                    +------------+------------+
                    |                         |
                    v                         v
             +-------------+           +-------------+
             |  Keycloak   |           |    Redis    |
             |    Auth     |           |             |
             +-------------+           +-------------+
                    |
                    | Authenticated
                    | Tenant Context
                    v
             +-------------+
             |   Qdrant    |
             | Vector DB   |
             +------+------+
                    |
                    | Relevant Chunks
                    v
             +-------------+
             | PostgreSQL  |
             | Authoritative|
             |   Content   |
             +------+------+
                    |
                    | Retrieved Context
                    v
             +-------------+
             | Hugging Face|
             |     LLM     |
             +------+------+
                    |
                    v
             +-------------+
             | RAG Answer  |
             | + Sources   |
             | + Trace ID  |
             +-------------+

                    MLflow
              ML Lifecycle /
             Evaluation Layer
```

## Running Services

| Service    | Purpose                       | Port |
| ---------- | ----------------------------- | ---: |
| Pharma API | FastAPI RAG API               | 8000 |
| Keycloak   | Authentication                | 8080 |
| MLflow     | ML lifecycle infrastructure   | 5000 |
| PostgreSQL | Database and document storage | 5432 |
| Qdrant     | Vector database               | 6333 |
| Redis      | Application infrastructure    | 6379 |

## API Endpoints

### Health Check

```text
GET /healthz
```

Returns:

```json
{
  "status": "ok"
}
```

### Readiness Check

```text
GET /readyz
```

The readiness endpoint verifies:

```text
PostgreSQL → OK
Qdrant     → OK
Redis      → OK
MLflow     → OK
Keycloak   → OK
```

### RAG Query

```text
POST /v1/rag/query
```

Example request:

```json
{
  "query": "What is paracetamol commonly used for?",
  "limit": 5
}
```

The endpoint requires a valid Keycloak Bearer access token.

Example successful response:

```json
{
  "trace_id": "d8b11435-ac6b-459b-8b30-1710c45eb121",
  "answer": "Paracetamol is commonly used to relieve mild to moderate pain and reduce fever.",
  "sources": [
    {
      "document_id": "490b2ada-e0c3-4512-895c-b38302ece781",
      "tenant_id": "f46efbed-bbdb-4d08-b312-bdd8263ac1fd",
      "chunk_index": 0,
      "score": 0.8685545
    },
    {
      "document_id": "4c1a106d-9094-491e-bb3a-1f3e4b7b6215",
      "tenant_id": "f46efbed-bbdb-4d08-b312-bdd8263ac1fd",
      "chunk_index": 0,
      "score": 0.8180586
    },
    {
      "document_id": "49bb17b0-1142-43de-95f5-6b92f232aed0",
      "tenant_id": "f46efbed-bbdb-4d08-b312-bdd8263ac1fd",
      "chunk_index": 0,
      "score": 0.8180586
    }
  ]
}
```

## Validation & Evidence

The current implementation has been tested end-to-end using the local Docker environment.

### Evidence 1 — Service Readiness

The `/readyz` endpoint successfully confirms that all major infrastructure dependencies are available:

* PostgreSQL
* Qdrant
* Redis
* MLflow
* Keycloak

**Screenshot:**

> Screenshot1 attached with this project mentioning the same.

Suggested caption:

**Figure 1 — Pharma RAG API readiness check showing PostgreSQL, Qdrant, Redis, MLflow and Keycloak as healthy.**

---

### Evidence 2 — Authenticated RAG Response

An authenticated RAG query was successfully executed through the API.

The response demonstrates:

* Successful authenticated request
* LLM-generated answer
* Unique trace ID
* Retrieved document sources
* Tenant ID associated with retrieved sources
* Similarity scores for retrieved chunks

**Screenshot:**

> Screenshot2 attached with this project mentioning the same.

Suggested caption:

**Figure 2 — Authenticated Pharma RAG query returning a grounded LLM response, trace ID and tenant-scoped retrieved sources.**

---

### Evidence 3 — Unsupported Information / No-Evidence Behavior

The system was also tested with a question about a fictional drug that is not present in the available information.

The response did not provide a fabricated treatment recommendation. Instead, the model indicated that the requested information was not available in the provided context.

**Screenshot:**

> Screenshot3 attached with this project mentioning the same.

Suggested caption:

**Figure 3 — RAG behavior for information not present in the available data, demonstrating non-hallucinatory response behavior.**

## Current Implementation Status

### Completed

The following components are currently implemented and working:

* Dockerized Pharma RAG application
* FastAPI REST API
* PostgreSQL integration
* Qdrant vector database integration
* Redis infrastructure
* Keycloak authentication
* JWT validation
* Server-side tenant extraction
* Server-side tenant filtering before vector retrieval
* PostgreSQL tenant validation during document retrieval
* Semantic vector search
* Hugging Face LLM integration
* Grounded RAG response generation
* Source metadata in API response
* Unique trace ID generation
* Health endpoint
* Readiness endpoint
* Docker Compose deployment
* Kubernetes deployment configuration
* Kubernetes ConfigMap and Secret configuration
* Kubernetes resource requests/limits
* Kubernetes liveness/readiness probe configuration
* MLflow service infrastructure

## Production Hardening Roadmap

The current implementation establishes the core secure RAG workflow. The following areas remain for complete production acceptance:

* Role-based and classification-based document authorization
* `allowed_roles` filtering in Qdrant
* Full multi-user and multi-tenant seed coverage
* Complete Keycloak-to-PostgreSQL identity mapping
* Formal `answered`, `insufficient_evidence` and `denied` response statuses
* Complete MLflow request-level tracing
* 150-question evaluation pipeline
* Retrieval and answer-quality evaluation metrics
* Complete T01-T10 acceptance test evidence
* Automated release-quality gates
* Successful Kubernetes image deployment
* Immutable image/commit traceability
* Kubernetes rollback validation
* Deliberately failing candidate release-block validation

## Security Considerations

Secrets are supplied through environment variables and Kubernetes Secrets.

The local `.env` file contains sensitive configuration and must not be committed to GitHub.

For production deployment, secrets should be managed using a dedicated secret-management solution.

## Project Structure

```text
Pharma-rag/
│
├── app/
│   ├── api/
│   ├── auth/
│   ├── db/
│   └── rag/
│
├── data/
├── deploy/
│   ├── docker/
│   └── k8s/
├── docs/
├── eval/
├── mlruns/
├── notebooks/
├── seed/
├── tests/
├── requirements.txt
└── README.md
```

## Conclusion

The current implementation demonstrates a working, containerized Pharma RAG pipeline with authentication, server-side tenant-aware retrieval, vector search, authoritative PostgreSQL content retrieval, grounded LLM generation, source metadata and request traceability.

The application and supporting infrastructure are currently running successfully through Docker Compose and have been validated through health, readiness, authenticated RAG and unsupported-information smoke tests.
