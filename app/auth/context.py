from dataclasses import dataclass


@dataclass(frozen=True)
class AuthorizationContext:
    """
    Trusted authorization context derived from the authenticated identity.

    These values must come from server-side authentication/authorization
    logic and must never be trusted directly from the client request.
    """

    user_id: str
    tenant_id: str
    roles: tuple[str, ...]