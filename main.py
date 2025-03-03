from contextlib import asynccontextmanager
from enum import Enum
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlmodel import Session, select
from database import create_db_and_tables, engine
from models import Task, TaskCreate, TaskPublic, TaskUpdate

description = """
#### Functionality:

* **Read tasks (id)**
* **Read tasks (skip/take)**
* **Create tasks**
* **Update tasks**
* **Delete tasks**
"""


class Tags(Enum):
    items = "items"


# manages context when to execute each code block based on yield split
@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup code happens before yield
    create_db_and_tables()
    yield
    # cleanup code happens after yield


# ensures we use a single session per request (yield gives control to route, then cleans up session implicitly)
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

app = FastAPI(
    version="0.0.1",
    title="TaskAPI",
    summary="a simple CRUD RESTful API.",
    description=description,
    lifespan=lifespan,
)


@app.get("/")
def read_root():
    return {
        "message": "Server running",
    }


@app.get("/tasks/{task_id}", response_model=TaskPublic, tags=[Tags.items])
def get_task(task_id: int, session: SessionDep) -> Task:
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get(
    "/tasks/",
    response_model=list[TaskPublic],
    tags=[Tags.items],
    summary="Get Tasks with pagination",
    description="Typically you wouldn't want to expose the entire DB. :D",
)
def get_tasks(
    session: SessionDep,
    skip: int = 0,
    take: Annotated[int, "whats this", Query(le=20)] = 5,
):
    tasks = session.exec(select(Task).offset(skip).limit(take)).all()
    return list(tasks)


@app.post(
    "/tasks/",
    response_model=TaskPublic,
    tags=[Tags.items],
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate, session: SessionDep):
    if not task.title.strip(): # generally each string should be stripped to begin with
        raise HTTPException(
            status_code=422, detail="Title cannot be empty or whitespace"
        )

    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.put("/tasks/{task_id}", response_model=TaskPublic, tags=[Tags.items])
def update_task(task_id: int, task: TaskUpdate, session: SessionDep):
    db_task = session.get(Task, task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    task_data = task.model_dump(exclude_unset=True)
    db_task.sqlmodel_update(task_data)

    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.delete("/tasks/{task_id}", tags=[Tags.items])
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
