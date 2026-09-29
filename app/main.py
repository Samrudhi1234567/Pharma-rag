import os

import httpx
import psycopg
import redis
from fastapi import FastAPI
from qdrant_client import QdrantClient
from app.api.rag import router as rag_router
from app.api.me import router as me_router
from app.api.documents import router as documents_router


app = FastAPI(
    title="Pharma RAG API",
    version="0.1.0",
)

app.include_router(rag_router)

app.include_router(me_router)

app.include_router(documents_router)

def check_postgres():
    conn = psycopg.connect(
        host=os.getenv("POSTGRES_HOST", "localhost"),
        port=int(os.getenv("POSTGRES_PORT", "5432")),
        dbname=os.getenv("POSTGRES_DB", "pharma_rag"),
        user=os.getenv("POSTGRES_USER", "pharma_user"),
        password=os.getenv("POSTGRES_PASSWORD"),
        connect_timeout=3,
    )
    conn.close()


def check_qdrant():
    client = QdrantClient(
        host=os.getenv("QDRANT_HOST", "localhost"),
        port=int(os.getenv("QDRANT_PORT", "6333")),
        timeout=3,
    )
    client.get_collections()


def check_redis():
    client = redis.Redis(
        host=os.getenv("REDIS_HOST", "localhost"),
        port=int(os.getenv("REDIS_PORT", "6379")),
        socket_connect_timeout=3,
    )
    client.ping()
    client.close()


def check_http(url: str):
    response = httpx.get(url, timeout=3)
    response.raise_for_status()


@app.get("/healthz")
def healthz():
    """Liveness check."""
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    """Dependency-aware readiness check."""

    checks = {}

    try:
        check_postgres()
        checks["postgres"] = "ok"
    except Exception as exc:
        checks["postgres"] = f"error: {type(exc).__name__}"

    try:
        check_qdrant()
        checks["qdrant"] = "ok"
    except Exception as exc:
        checks["qdrant"] = f"error: {type(exc).__name__}"

    try:
        check_redis()
        checks["redis"] = "ok"
    except Exception as exc:
        checks["redis"] = f"error: {type(exc).__name__}"

    try:
        mlflow_host = os.getenv("MLFLOW_HOST", "localhost")
        mlflow_port = os.getenv("MLFLOW_PORT", "5000")
        check_http(f"http://{mlflow_host}:{mlflow_port}/version")
        checks["mlflow"] = "ok"
    except Exception as exc:
        checks["mlflow"] = f"error: {type(exc).__name__}"

    try:
        keycloak_host = os.getenv("KEYCLOAK_HOST", "localhost")
        keycloak_port = os.getenv("KEYCLOAK_PORT", "8080")
        check_http(f"http://{keycloak_host}:{keycloak_port}/realms/master")
        checks["keycloak"] = "ok"
    except Exception as exc:
        checks["keycloak"] = f"error: {type(exc).__name__}"

    ready = all(value == "ok" for value in checks.values())

    return {
        "status": "ready" if ready else "not_ready",
        "checks": checks,
    }