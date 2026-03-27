from fastapi import Depends
from sqlalchemy.orm import Session

from models import Comment
from core.database import get_db


class CommentRepository:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create(self, task_id: int, text: str) -> Comment:
        comment = Comment(task_id=task_id, text=text)
        self.db.add(comment)
        self.db.commit()
        self.db.refresh(comment)
        return comment

    def get_all_by_task_id(self, task_id: int) -> list[Comment]:
        return (
            self.db.query(Comment)
            .filter(Comment.task_id == task_id)
            .order_by(Comment.created_at.desc())
            .all()
        )
    
    def get_by_id(self, task_id: int, comment_id: int) -> Comment | None:
        return (
            self.db.query(Comment)
            .filter(
                Comment.id == comment_id,
                Comment.task_id == task_id
            )
            .first()
        )