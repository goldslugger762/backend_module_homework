from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from dependency import PaginationDep, check_headers
from schemas.tasks import TaskSchema, UpdateTaskSchema, CreateTaskSchema
from services.tasks import TaskService


router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", dependencies=[Depends(check_headers)])
def add_task(
        payload: CreateTaskSchema,
        service: TaskService = Depends()
) -> JSONResponse:
    add_result = service.add_task(payload)

    return JSONResponse({
        "message": "The task has been added",
        "task": jsonable_encoder(add_result)
    }, status_code=status.HTTP_201_CREATED)


@router.get("/{task_id}")
def get_task(
        task_id: int,
        service: TaskService = Depends()
) -> JSONResponse:
    get_result = service.get_task_by_id(task_id)

    if get_result:
        return JSONResponse(jsonable_encoder(get_result), status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.get("/")
def get_tasks_collection(
        pagination: PaginationDep,
        service: TaskService = Depends()
) -> list[TaskSchema]:
    get_result = service.get_tasks(pagination.limit, pagination.offset)
    return get_result


@router.patch("/{task_id}")
def update_task(
        task_id: int,
        payload: UpdateTaskSchema,
        service: TaskService = Depends()
):
    update_result = service.update_task(task_id, payload)

    if update_result:
        return JSONResponse(jsonable_encoder(update_result), status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )


@router.delete("/{task_id}")
def delete_task(
        task_id: int,
        service: TaskService = Depends()
) -> JSONResponse:
    delete_result = service.delete_task(task_id)

    if delete_result:
        return JSONResponse({
            "status": "success"
        }, status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )