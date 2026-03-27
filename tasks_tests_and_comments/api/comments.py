from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from services import CommentService
from schemas import CommentSchema, CreateCommentSchema


router = APIRouter(prefix="/v1/tasks", tags=["comments"])


@router.post("/{task_id}/comments")
def add_comment(
    task_id: int,
    payload: CreateCommentSchema,
    service: CommentService = Depends()
) -> JSONResponse:
    result = service.add_comment(task_id, payload)

    return JSONResponse({
        "message": "Comment added",
        "comment": jsonable_encoder(result)
    }, status_code=status.HTTP_201_CREATED)


@router.get("/{task_id}/comments")
def get_comments(
    task_id: int,
    service: CommentService = Depends()
) -> list[CommentSchema]:
    return service.get_comments(task_id)

@router.get("/{task_id}/comments/{comment_id}")
def get_comment_by_id(
    task_id: int,
    comment_id: int,
    service: CommentService = Depends()
) -> CommentSchema:
    return service.get_comment_by_id(task_id, comment_id)