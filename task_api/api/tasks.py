from fastapi import APIRouter, Response, status, Depends
from fastapi.responses import JSONResponse
from typing import List

from schemas import BaseTask, TaskCreate, TaskUpdate
from services import TaskService


router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)


@router.get("/", response_model=List[BaseTask], status_code=status.HTTP_200_OK)
def get_tasks(service: TaskService = Depends()):
    result = service.get_all_tasks()

    if not result:
        return JSONResponse(
            {
                "status": "error",
                "message": "Не найдено тасок"
            },
            status_code=status.HTTP_404_NOT_FOUND
        )

    return result


@router.get("/{task_id}", response_model=BaseTask, status_code=status.HTTP_200_OK)
def get_task(task_id: int, service: TaskService = Depends()):
    result = service.get_task(task_id)

    if not result:
        return JSONResponse(
            {"message": "Таска не найдена"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    return result


@router.post("/", response_model=BaseTask, status_code=status.HTTP_201_CREATED)
def create_task(response: Response, task: TaskCreate, service: TaskService = Depends()):
    result = service.add_task(task)

    response.status_code = status.HTTP_201_CREATED

    return result


@router.put("/{task_id}", response_model=BaseTask, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TaskUpdate, service: TaskService = Depends()):
    result = service.update_task(task_id, task)

    if not result:
        return JSONResponse(
            {"message": "Таска не найдена"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    return result


@router.delete("/{task_id}", status_code=status.HTTP_200_OK)
def delete_task(task_id: int, service: TaskService = Depends()):
    result = service.delete_task(task_id)

    if not result:
        return JSONResponse(
            {"message": "Таска не найдена"},
            status_code=status.HTTP_404_NOT_FOUND
        )

    return {"message": "Задача удалена"}