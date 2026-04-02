from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Task
from schemas.tasks import CreateTaskSchema, UpdateTaskSchema
from core.database import get_db


class TaskRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all(
        self,
        owner_id: int,
        limit: int,
        offset: int
    ):
        result = await self.db.execute(
            select(Task)
            .where(Task.owner_id == owner_id)
            .limit(limit)
            .offset(offset)
        )
        return list(result.scalars().all())

    async def get_by_id(self, task_id: int) -> Optional[Task]:
        result = await self.db.execute(
            select(Task).where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    async def create(self, task_data: dict) -> Task:
        task_db = Task(**task_data)
        self.db.add(task_db)
        await self.db.commit()
        await self.db.refresh(task_db)
        return task_db

    async def update(self, task_id: int, task: UpdateTaskSchema) -> Optional[Task]:
        task_db = await self.get_by_id(task_id)
        if not task_db:
            return None

        update_data = task.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(task_db, field, value)

        await self.db.commit()
        await self.db.refresh(task_db)
        return task_db

    async def delete(self, task_id: int) -> bool:
        task = await self.get_by_id(task_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        return True