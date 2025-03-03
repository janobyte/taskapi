from enum import Enum
from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, status
from sqlmodel import select

from taskapi.db import SessionDep
from taskapi.models.task import Task, TaskCreate, TaskPublic, TaskUpdate


class Tags(Enum):
    items = "items"


router = APIRouter(prefix="/task")


@router.get("/{task_id}", response_model=TaskPublic, tags=[Tags.items])
def get_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get(
    "/",
    response_model=list[TaskPublic],
    tags=[Tags.items],
    summary="Get Tasks with pagination",
    description="Typically you wouldn't want to expose the entire DB. :D",
)
def get_tasks(
    session: SessionDep,
    skip: int = 0,
    take: Annotated[int, Query(le=20)] = 5,
):
    tasks = session.exec(select(Task).offset(skip).limit(take)).all()
    return list(tasks)


@router.post(
    "/",
    response_model=TaskPublic,
    tags=[Tags.items],
    status_code=status.HTTP_201_CREATED,
)
def create_task(task: TaskCreate, session: SessionDep):
    if not task.title.strip():  # generally each string should be stripped to begin with
        raise HTTPException(status_code=422, detail="Title cannot be empty or whitespace")

    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.put("/{task_id}", response_model=TaskPublic, tags=[Tags.items])
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


@router.delete("/{task_id}", tags=[Tags.items])
def delete_task(task_id: int, session: SessionDep):
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(task)
    session.commit()
    return {"ok": True}
