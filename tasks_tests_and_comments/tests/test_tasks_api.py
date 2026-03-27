from fastapi.testclient import TestClient
from main import app
from core.database import get_db


def test_create_task(db_session):
    # Подменяем БД на тестовую
    app.dependency_overrides[get_db] = lambda: db_session

    test_client = TestClient(app)

    payload = {
        "title": "Test task from API"
    }

    response = test_client.post(
        "/tasks/",
        json=payload,
        headers={"auth-token": "123"}
    )

    assert response.status_code == 201

    data = response.json()
    assert data["message"] == "The task has been added"
    assert data["task"]["title"] == payload["title"]
    assert "id" in data["task"]
