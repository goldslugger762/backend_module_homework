from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class CreateTaskSchema(BaseModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False


class UpdateTaskSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None