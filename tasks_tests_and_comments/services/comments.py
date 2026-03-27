from fastapi import Depends

from repositories.comments import CommentRepository
from repositories.tasks import TaskRepository
from schemas import CommentSchema, CreateCommentSchema
from core.exceptions import TaskNotFoundException, CommentNotFoundException


class CommentService:
    def __init__(
        self,
        comment_repo: CommentRepository = Depends(),
        task_repo: TaskRepository = Depends()
    ):
        self.comment_repo = comment_repo
        self.task_repo = task_repo

    def _get_task_or_404(self, task_id: int):
        task = self.task_repo.get_by_id(task_id)
        if not task:
            raise TaskNotFoundException(task_id=task_id)
        return task

    def add_comment(self, task_id: int, payload: CreateCommentSchema) -> CommentSchema:
        self._get_task_or_404(task_id)
        return self.comment_repo.create(task_id, payload.text)

    def get_comments(self, task_id: int) -> list[CommentSchema]:
        self._get_task_or_404(task_id)
        return self.comment_repo.get_all_by_task_id(task_id)
    
    def get_comment_by_id(self, task_id: int, comment_id: int) -> CommentSchema:
        self._get_task_or_404(task_id)
        
        comment = self.comment_repo.get_by_id(task_id, comment_id)
        
        if not comment:
            raise CommentNotFoundException(comment_id=comment_id)
        
        return comment