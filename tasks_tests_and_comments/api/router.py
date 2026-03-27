from fastapi import APIRouter, status
from fastapi.responses import JSONResponse

from api import tasks_router
from api import auth_router
from api import comments_router

common_router = APIRouter()


@common_router.get("/")
def root():
    return JSONResponse(
        {"Hello": "World"},
        status_code=status.HTTP_200_OK
    )


common_router.include_router(tasks_router)
common_router.include_router(auth_router)
common_router.include_router(comments_router)