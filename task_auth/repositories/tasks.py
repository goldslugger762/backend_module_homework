from typing import List, Optional

from fastapi import Depends
from sqlalchemy.orm import Session

from models import Task
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema
from core.database import get_db


class TaskRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self, limit: int, offset: int) -> List[Task]:
        return self.db.query(Task).limit(limit).offset(offset).all()

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def create(self, task: CreateTaskSchema) -> Task:
        task_db = Task(**task.model_dump())
        self.db.add(task_db)
        self.db.commit()
        self.db.refresh(task_db)
        return task_db

    def update(self, task_id: int, task: UpdateTaskSchema) -> Optional[Task]:
        task_db = self.get_by_id(task_id)
        if not task_db:
            return None

        update_data = task.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task_db, field, value)

        self.db.commit()
        self.db.refresh(task_db)
        return task_db

    def delete(self, task_id: int) -> bool:
        task = self.get_by_id(task_id)
        if not task:
            return False

        self.db.delete(task)
        self.db.commit()
        return True