from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import SQLModel, Session, create_engine, select
from models import Todo
from typing import List

DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(DATABASE_URL, echo=False)

app = FastAPI(title="Simple Todo API")

# Allow the frontend dev server (Vite) to talk to this API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create DB + tables if they don't exist
SQLModel.metadata.create_all(engine)

@app.get("/todos", response_model=List[Todo])
def list_todos():
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return todos

@app.post("/todos", response_model=Todo)
def create_todo(todo: Todo):
    # We accept a Todo without id; SQLModel will fill id
    with Session(engine) as session:
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, updated: Todo):
    with Session(engine) as session:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        # Only update fields we expect: title and done
        db_todo.title = updated.title
        db_todo.done = updated.done
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail="Todo not found")
        session.delete(db_todo)
        session.commit()
        return {"ok": True}