import pytest
from unittest.mock import MagicMock

from services import TaskService
from schemas import CreateTaskSchema
from models import Task


@pytest.fixture
def mock_task_repo():
    return MagicMock()


@pytest.fixture
def task_service(mock_task_repo):
    return TaskService(repository=mock_task_repo)


def test_add_task(task_service, mock_task_repo):
    payload = CreateTaskSchema(title="Test task")

    mock_task = Task(id=1, title="Test task")
    mock_task_repo.create.return_value = mock_task

    result = task_service.add_task(payload)

    mock_task_repo.create.assert_called_once_with(payload)
    assert result == mock_task