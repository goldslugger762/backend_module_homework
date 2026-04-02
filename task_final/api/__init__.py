from api.tasks import router as tasks_router
from api.auth import router as auth_router
from api.comments import router as comments_router
from api.system import router as system_router
from api.router import common_router

__all__ = (
    "tasks_router",
    "auth_router",
    "comments_router",
    "system_router",
    "common_router",
)