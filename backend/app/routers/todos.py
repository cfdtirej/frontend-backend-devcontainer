from typing import Annotated

from fastapi import APIRouter, Body, Path, status
from fastapi.exceptions import HTTPException as HttpException

from app.schemas.todos import Todo, TodoItem

router = APIRouter(prefix="/todos", tags=["todos"])

todo_list = [
    Todo(id=1, title="Todo 1", description="This is the first task", completed=False),
    Todo(id=2, title="Todo 2", description="This is the second task", completed=False),
    Todo(id=3, title="Todo 3", description="This is the third task", completed=False),
]


@router.get("", status_code=status.HTTP_200_OK)
def list_todos() -> list[Todo]:
    return todo_list


@router.post("", status_code=status.HTTP_201_CREATED)
def create_todo(
    todo_detail: Annotated[TodoItem, Body(...)]
) -> Todo:
    max_id = todo_list[-1].id
    new_todo = Todo(id=max_id + 1, **todo_detail.model_dump())
    todo_list.append(new_todo)
    return new_todo


@router.put("/{id}", status_code=status.HTTP_200_OK)
def update_todo(
    id: Annotated[int, Path(...)],
    todo_detail: Annotated[TodoItem, Body(...)]
) -> Todo:
    for todo in todo_list:
        if todo.id == id:
            todo.title = todo_detail.title
            todo.description = todo_detail.description
            todo.completed = todo_detail.completed
            return todo

    raise HttpException(status_code=404, detail="Todo not found")


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo():
    for i, todo in enumerate(todo_list):
        if todo.id == id:
            todo_list.pop(i)
            return {"message": "Todo deleted"}

    raise HttpException(status_code=404, detail="Todo not found")
