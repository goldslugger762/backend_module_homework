from pydantic import BaseModel, Field
from datetime import datetime


class CommentSchema(BaseModel):
    id: int
    text: str
    task_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class CreateCommentSchema(BaseModel):
    text: str = Field(min_length=1, max_length=500)
