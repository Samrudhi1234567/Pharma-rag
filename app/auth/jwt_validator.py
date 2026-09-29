import os
from functools import lru_cache

import jwt
from jwt import PyJWKClient


KEYCLOAK_INTERNAL_URL = os.getenv(
    "KEYCLOAK_INTERNAL_URL",
    "http://keycloak:8080",
)

KEYCLOAK_ISSUER = os.getenv(
    "KEYCLOAK_ISSUER",
    "http://localhost:8080/realms/pharma-rag",
)

JWKS_URL = (
    f"{KEYCLOAK_INTERNAL_URL}/realms/pharma-rag"
    "/protocol/openid-connect/certs"
)

EXPECTED_CLIENT_ID = os.getenv(
    "KEYCLOAK_CLIENT_ID",
    "pharma-rag-api",
)


@lru_cache(maxsize=1)
def get_jwk_client():
    return PyJWKClient(JWKS_URL)


def validate_access_token(token: str) -> dict:
    signing_key = get_jwk_client().get_signing_key_from_jwt(token)

    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        issuer=KEYCLOAK_ISSUER,
        options={
            "verify_aud": False,
        },
    )

    if payload.get("azp") != EXPECTED_CLIENT_ID:
        raise ValueError("Invalid token client")

    return payload