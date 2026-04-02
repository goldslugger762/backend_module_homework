from typing import List, Annotated

from fastapi import APIRouter, Depends, UploadFile, File, Form
from starlette.responses import JSONResponse

from services import TaskService
from schemas import TaskSchema
from dependency import CurrentUserDep, PaginationDep


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/")
async def create_task(
    current_user: CurrentUserDep,
    title: Annotated[str, Form(min_length=1, max_length=255)],
    description: Annotated[str | None, Form()] = None,
    image: Annotated[UploadFile | None, File()] = None,
    service: TaskService = Depends(TaskService),
) -> TaskSchema:
    return await service.add_task(
        title=title,
        description=description,
        owner_id=current_user.id,
        image=image
    )


@router.get("/")
async def get_tasks(
    current_user: CurrentUserDep,
    pagination: PaginationDep,
    service: TaskService = Depends(TaskService),
):
    return await service.get_tasks(
        owner_id=current_user.id,
        limit=pagination.limit,
        offset=pagination.offset
    )


@router.get("/{task_id}")
async def get_task(
    task_id: int,
    service: TaskService = Depends(TaskService),
) -> TaskSchema:
    return await service.get_task_by_id(task_id)

@router.patch("/{task_id}")
async def update_task(
    task_id: int,
    current_user: CurrentUserDep,
    title: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    is_completed: Annotated[bool | None, Form()] = None,
    image: Annotated[UploadFile | None, File()] = None,
    service: TaskService = Depends(TaskService),
) -> TaskSchema:
    return await service.update_task(
        task_id=task_id,
        owner_id=current_user.id,
        title=title,
        description=description,
        is_completed=is_completed,
        image=image
    )

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: CurrentUserDep,
    service: TaskService = Depends(TaskService),
) -> JSONResponse:
    await service.delete_task(task_id, current_user.id)
    return JSONResponse(status_code=200, content={"message": "Task deleted"})

@router.post("/{task_id}/upload-avatar")
async def upload_task_avatar(
    task_id: int,
    file: Annotated[UploadFile, File()],
    current_user: CurrentUserDep,
    service: TaskService = Depends(TaskService),
):
    return await service.upload_avatar(task_id, current_user.id, file)