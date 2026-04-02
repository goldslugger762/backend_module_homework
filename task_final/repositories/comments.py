from typing import List, Optional

from fastapi import Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from models import Comment
from core.database import get_db


class CommentRepository:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def create(self, task_id: int, text: str) -> Comment:
        comment = Comment(task_id=task_id, text=text)
        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def get_all_by_task_id(self, task_id: int) -> List[Comment]:
        result = await self.db.execute(
            select(Comment)
            .where(Comment.task_id == task_id)
            .order_by(desc(Comment.created_at))
        )
        return list(result.scalars().all())

    async def get_by_id(self, task_id: int, comment_id: int) -> Optional[Comment]:
        result = await self.db.execute(
            select(Comment).where(
                Comment.id == comment_id,
                Comment.task_id == task_id
            )
        )
        return result.scalar_one_or_none()