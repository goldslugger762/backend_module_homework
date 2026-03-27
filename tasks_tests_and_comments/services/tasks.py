from fastapi import Depends

from schemas.tasks import TaskSchema, UpdateTaskSchema, CreateTaskSchema
from repositories.tasks import TaskRepository
from core.exceptions import TaskNotFoundException


class TaskService:
    def __init__(self, repository: TaskRepository = Depends()):
        self.repo = repository

    def add_task(self, new_task: CreateTaskSchema):
        return self.repo.create(new_task)

    def get_task_by_id(self, task_id: int) -> TaskSchema:
        task_db = self.repo.get_by_id(task_id)

        if not task_db:
            raise TaskNotFoundException(task_id=task_id)

        return task_db

    def get_tasks(self, limit: int, offset: int) -> list[TaskSchema]:
        return self.repo.get_all(limit, offset)

    def update_task(self, task_id: int, payload: UpdateTaskSchema) -> TaskSchema:
        db_task = self.repo.update(task_id, payload)

        if not db_task:
            raise TaskNotFoundException(task_id=task_id)

        return db_task

    def delete_task(self, task_id: int) -> bool:
        result = self.repo.delete(task_id)

        if not result:
            raise TaskNotFoundException(task_id=task_id)

        return result