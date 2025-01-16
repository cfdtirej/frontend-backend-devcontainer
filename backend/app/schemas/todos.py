from pydantic import BaseModel


class TodoItem(BaseModel):
    title: str
    description: str
    completed: bool


class Todo(TodoItem):
    id: int
