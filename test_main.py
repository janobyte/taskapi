from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlmodel import SQLModel, Session, create_engine
from main import app, get_session


client = TestClient(app)

sqlite_url = "sqlite:///:memory:"
connect_args = {"check_same_thread": False}
engine = create_engine(
    sqlite_url, echo=True, connect_args=connect_args, poolclass=StaticPool
)

SQLModel.metadata.create_all(engine)


def override_get_session():
    with Session(engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session


def test_read_main():
    """
    Health check test.
    """
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Server running"}


"""
Test section for create task:
"""


def test_create_task():
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    created_task = response.json()
    assert created_task["title"] == task_data["title"]
    assert created_task["description"] == task_data["description"]
    assert created_task["completed"] == task_data["completed"]
    assert "id" in created_task


# missing entire body
def test_create_task_missing_body():
    response = client.post("/tasks/", json={})  # Empty body
    assert response.status_code == 422


# missing title in body
def test_create_task_missing_title():
    task_data = {
        "description": "Task without a title",
        "completed": False,
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422


# wrong data types
def test_create_task_invalid_types():
    task_data = {
        "title": 123,  # Should be a string
        "description": True,  # Should be a string or None
        "completed": "yes",  # Should be a boolean
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422


# empty title string
def test_create_task_empty_title():
    task_data = {
        "title": "",
        "description": "This task has an empty title",
        "completed": False,
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422


# empty (as in whitespaced) title string
def test_create_task_whitespace_title():
    task_data = {
        "title": " ",
        "description": "This task has a whitespace title",
        "completed": False,
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422


# title string is too long
def test_create_task_long_title():
    long_title = "c" * 51  # char limit is 50
    task_data = {
        "title": long_title,
        "description": "Task with a very long title",
        "completed": False,
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 422
