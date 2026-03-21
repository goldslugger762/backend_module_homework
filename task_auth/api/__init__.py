from api.tasks import router as tasks_router
from api.auth import router as auth_router
from api.router import common_router

__all__ = (
    "tasks_router",
    "common_router",
    "auth_router"
)