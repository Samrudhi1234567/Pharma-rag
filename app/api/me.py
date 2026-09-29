from fastapi import APIRouter, Depends

from app.auth.context import AuthorizationContext
from app.auth.dependencies import get_authorization_context


router = APIRouter()


@router.get("/v1/me")
def get_current_user(
    auth_context: AuthorizationContext = Depends(
        get_authorization_context
    ),
):
    return {
        "user_id": auth_context.user_id,
        "tenant_id": auth_context.tenant_id,
        "roles": list(auth_context.roles),
    }