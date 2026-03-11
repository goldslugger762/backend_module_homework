from pydantic import BaseModel, Field, field_validator
from typing import Optional


class TaskBase(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: bool = False

    @field_validator("title")
    def validate_title(cls, value):
        if value.strip() == "":
            raise ValueError("Заголовок не может быть пустым")
        if value.isdigit():
            raise ValueError("Заголовок не может содержать одни цифры")
        return value

    @field_validator("description")
    def validate_description(cls, value):
        if value is not None and len(value.strip()) < 5:
            raise ValueError("В описании должно быть как минимум 5 символов")
        return value


class TaskCreate(TaskBase):
    id: int = Field(gt=0)


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    completed: Optional[bool]

    @field_validator("title")
    def validate_title(cls, value):
        if value is not None and value.strip() == "":
            raise ValueError("Заголовок не может быть пустым")
        return value


class BaseTask(TaskBase):
    id: int