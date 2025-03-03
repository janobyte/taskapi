from contextlib import asynccontextmanager
from fastapi import FastAPI
from taskapi.db import create_db_and_tables
from taskapi.routes import task

description = """
#### Functionality:

* **Read tasks (id)**
* **Read tasks (skip/take)**
* **Create tasks**
* **Update tasks**
* **Delete tasks**
"""


@asynccontextmanager
async def lifespan(app):
    create_db_and_tables()
    yield


app = FastAPI(
    version="0.0.1",
    title="TaskAPI",
    summary="a simple CRUD RESTful API.",
    description=description,
    lifespan=lifespan,
)
app.include_router(task.router)


@app.get("/")
def read_root():
    return {
        "message": "Server running",
    }
