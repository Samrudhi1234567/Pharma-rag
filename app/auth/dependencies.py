from fastapi import Header, HTTPException

from app.auth.context import AuthorizationContext
from app.auth.jwt_validator import validate_access_token


def get_authorization_context(
    authorization: str | None = Header(default=None),
) -> AuthorizationContext:

    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Authorization header is required",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Bearer token is required",
        )

    token = authorization.removeprefix("Bearer ").strip()

    if not token:
        raise HTTPException(
            status_code=401,
            detail="Bearer token is required",
        )

    try:
        payload = validate_access_token(token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
        )

    user_id = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token subject is missing",
        )

    groups = payload.get("groups", [])

    tenant_ids = []

    for group in groups:
        if group.startswith("tenant-"):
            tenant_ids.append(group.removeprefix("tenant-"))

    if len(tenant_ids) != 1:
        raise HTTPException(
            status_code=403,
            detail="Token must contain exactly one tenant",
        )

    tenant_id = tenant_ids[0]

    roles = tuple(
        payload.get("realm_access", {}).get("roles", [])
    )

    return AuthorizationContext(
        user_id=user_id,
        tenant_id=tenant_id,
        roles=roles,
    )