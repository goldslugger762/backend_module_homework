import pytest
from unittest.mock import MagicMock

from services import TaskService
from schemas import CreateTaskSchema
from models import Task
from repositories import TaskRepository


@pytest.fixture
def mock_task_repo():
    return MagicMock(spec=TaskRepository)


@pytest.fixture
def task_service(mock_task_repo):
    return TaskService(repository=mock_task_repo)


def test_create_task(task_service, mock_task_repo):
    """Unit-тест для TaskService.create_task (с моком репозитория)"""
    payload = CreateTaskSchema(title="Test task")

    mock_task = Task(id=1, title="Test task")
    mock_task_repo.create.return_value = mock_task

    result = task_service.add_task(payload)

    mock_task_repo.create.assert_called_once()
    args, _ = mock_task_repo.create.call_args

    assert args[0] == payload
    assert result.id == mock_task.id
    assert result.title == mock_task.title


def test_add_task_returns_none(task_service, mock_task_repo):
    """Дополнительный тест: сервис возвращает None, если репозиторий вернул None"""
    payload = CreateTaskSchema(title="Test task")
    mock_task_repo.create.return_value = None

    result = task_service.add_task(payload)

    assert result is None