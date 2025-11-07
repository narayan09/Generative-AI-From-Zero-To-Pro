from fastapi import FastAPI, HTTPException, status # pyright: ignore[reportMissingImports]
from pydantic import BaseModel
from typing import List
import json, os

app = FastAPI(title="FastAPI Todo App")

# JSON file path
TODO_FILE = "todos.json"


# ✅ Model
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


# ✅ Helper functions to load/save JSON data
def load_todos() -> List[dict]:
    if not os.path.exists(TODO_FILE):
        return []
    with open(TODO_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def save_todos(todos: List[dict]):
    with open(TODO_FILE, "w") as f:
        json.dump(todos, f, indent=4)


# ✅ CREATE (POST)
@app.post("/todos", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo):
    todos = load_todos()

    # Prevent duplicate ID
    for t in todos:
        if t["id"] == todo.id:
            raise HTTPException(status_code=400, detail="Todo ID already exists")

    todos.append(todo.dict())
    save_todos(todos)
    return {"message": "Todo created!", "todo": todo}


# ✅ READ ALL (GET)
@app.get("/todos", response_model=List[Todo])
def get_all_todos():
    return load_todos()


# ✅ READ ONE (GET)
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    todos = load_todos()
    for todo in todos:
        if todo["id"] == todo_id:
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


# ✅ UPDATE (PUT)
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    todos = load_todos()
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos[index] = updated_todo.dict()
            save_todos(todos)
            return {"message": "Todo updated!", "todo": updated_todo}
    raise HTTPException(status_code=404, detail="Todo not found")


# ✅ DELETE (DELETE)
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    todos = load_todos()
    for index, todo in enumerate(todos):
        if todo["id"] == todo_id:
            deleted = todos.pop(index)
            save_todos(todos)
            return {"message": "Todo deleted!", "deleted_todo": deleted}
    raise HTTPException(status_code=404, detail="Todo not found")
