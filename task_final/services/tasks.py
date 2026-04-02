import uuid

from fastapi import Depends, UploadFile

from schemas.tasks import TaskSchema
from repositories.tasks import TaskRepository
from core.exceptions import (
    TaskNotFoundException,
    InvalidImageFormatException,
    ForbiddenException
)
from adapters.storage.base import StorageAdapter
from core.adapters import get_storage


class TaskService:
    def __init__(
        self,
        repository: TaskRepository = Depends(TaskRepository),
        storage: StorageAdapter = Depends(get_storage)
    ):
        self.repo = repository
        self.storage = storage

    async def add_task(
        self,
        title: str,
        description: str | None,
        owner_id: int,
        image: UploadFile | None = None
    ) -> TaskSchema:

        img_url = None

        if image is not None:
            content = await image.read()
            ext = image.filename.split('.')[-1] if image.filename else "bin"

            if ext not in ("jpeg", "jpg", "png"):
                raise InvalidImageFormatException(["jpeg", "jpg", "png"])

            key = f"tasks/{uuid.uuid4()}.{ext}"
            img_url = await self.storage.upload(
                content,
                key,
                image.content_type or "application/octet-stream"
            )

        return await self.repo.create({
            "title": title,
            "description": description,
            "owner_id": owner_id,
            "img_url": img_url
        })

    async def get_task_by_id(self, task_id: int) -> TaskSchema:
        task_db = await self.repo.get_by_id(task_id)

        if not task_db:
            raise TaskNotFoundException(task_id=task_id)

        return task_db

    async def get_tasks(
        self,
        owner_id: int,
        limit: int,
        offset: int
    ):
        tasks = await self.repo.get_all(owner_id, limit, offset)
        return [
            TaskSchema(
                id=t.id,
                title=t.title,
                description=t.description,
                is_completed=t.is_completed,
                owner_id=t.owner_id,
                img_url=t.img_url,
                created_at=t.created_at,
                updated_at=t.updated_at
            )
            for t in tasks
        ]

    async def update_task(
        self,
        task_id: int,
        owner_id: int,
        title: str | None = None,
        description: str | None = None,
        is_completed: bool | None = None,
        image: UploadFile | None = None
    ) -> TaskSchema:

        task = await self.repo.get_by_id(task_id)

        if not task:
            raise TaskNotFoundException(task_id=task_id)

        if task.owner_id != owner_id:
            raise ForbiddenException("Вы не владелец задачи")

        update_data = {}

        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if is_completed is not None:
            update_data["is_completed"] = is_completed

        if image is not None:
            content = await image.read()
            ext = image.filename.split('.')[-1] if image.filename else "bin"

            if ext not in ("jpeg", "jpg", "png"):
                raise InvalidImageFormatException(["jpeg", "jpg", "png"])

            key = f"tasks/{uuid.uuid4()}.{ext}"
            img_url = await self.storage.upload(
                content,
                key,
                image.content_type or "application/octet-stream"
            )

            update_data["img_url"] = img_url

        updated_task = await self.repo.update(task_id, update_data)

        return updated_task

    async def delete_task(self, task_id: int, owner_id: int) -> None:
        task = await self.repo.get_by_id(task_id)

        if not task:
            raise TaskNotFoundException(task_id=task_id)

        if task.owner_id != owner_id:
            raise ForbiddenException("Вы не владелец задачи")

        await self.repo.delete(task_id)

    async def upload_avatar(
        self,
        task_id: int,
        owner_id: int,
        file: UploadFile
    ) -> dict:

        task = await self.repo.get_by_id(task_id)

        if not task:
            raise TaskNotFoundException(task_id=task_id)

        if task.owner_id != owner_id:
            raise ForbiddenException("Вы не владелец задачи")

        content = await file.read()
        ext = file.filename.split('.')[-1] if file.filename else "bin"

        if ext not in ("jpeg", "jpg", "png"):
            raise InvalidImageFormatException(["jpeg", "jpg", "png"])

        key = f"tasks/avatars/{uuid.uuid4()}.{ext}"

        img_url = await self.storage.upload(
            content,
            key,
            file.content_type or "application/octet-stream"
        )

        await self.repo.update(task_id, {"img_url": img_url})

        return {"img_url": img_url}