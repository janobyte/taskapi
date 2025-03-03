from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=50, index=True)
    description: str | None = None
    completed: bool = Field(default=False, index=True)


class Task(TaskBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class TaskCreate(TaskBase):
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "My task!",
                    "description": "An urgent task.",
                    "completed": False,
                }
            ]
        }
    }  # type: ignore


class TaskPublic(TaskBase):
    id: int


class TaskUpdate(SQLModel):
    title: str | None = None
    description: str | None = None
    completed: bool | None = None
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "My task!",
                    "description": "An urgent task.",
                    "completed": False,
                }
            ]
        }
    }  # type: ignore
