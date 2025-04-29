# Context variables
from contextvars import ContextVar
from typing import Optional


current_user_id: ContextVar[Optional[str]] = ContextVar("current_user_id", default=None)
current_tenant_id: ContextVar[Optional[str]] = ContextVar(
    "current_tenant_id", default=None
)
current_project_id: ContextVar[Optional[str]] = ContextVar(
    "current_project_id", default=None
)

current_bearer_token: ContextVar[Optional[str]] = ContextVar(
    "current_bearer_token", default=None
)
