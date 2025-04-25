# main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from . import crud, models, schemas

app = FastAPI()

# Базовая операция для получения списка todos
@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Возвращает список всех TodoList'ов, начиная с позиции skip и ограничивая выборку значением limit.
    """
    todos = crud.get_todos(db, skip=skip, limit=limit)
    return todos

# Операция для создания нового TodoList
@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """
    Создает новый TodoList и возвращает созданный объект.
    """
    return crud.create_todo(db=db, todo=todo)

# Операция для обновления существующих записей
@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    """
    Обновляет существующую запись TodoList по ID.
    """
    return crud.update_todo(db=db, todo_id=todo_id, todo=todo)

# Удаляет конкретный TodoList по ID
@app.delete("/todos/{todo_id}", response_model=dict)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """
    Удаляет TodoList по заданному идентификатору.
    """
    crud.delete_todo(db=db, todo_id=todo_id)
    return {"detail": "Todo deleted successfully"}

# Для элементов (Items) аналогично делаем GET, POST, PUT, DELETE
@app.get("/todos/{todo_id}/items/", response_model=list[schemas.Item])
def read_items(todo_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Читает все Items, принадлежащие указанному TodoList.
    """
    items = crud.get_items(db, todo_id, skip=skip, limit=limit)
    return items

@app.post("/todos/{todo_id}/items/", response_model=schemas.Item)
def create_item(todo_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Создает новый элемент (Item) в выбранном TodoList.
    """
    return crud.create_item(db=db, item=item, todo_id=todo_id)

@app.put("/todos/{todo_id}/items/{item_id}", response_model=schemas.Item)
def update_item(todo_id: int, item_id: int, item: schemas.ItemUpdate, db: Session = Depends(get_db)):
    """
    Обновляет элемент (Item) по его ID.
    """
    return crud.update_item(db=db, item_id=item_id, item=item)

@app.delete("/todos/{todo_id}/items/{item_id}", response_model=dict)
def delete_item(todo_id: int, item_id: int, db: Session = Depends(get_db)):
    """
    Удаляет элемент (Item) по его ID.
    """
    crud.delete_item(db=db, item_id=item_id)
    return {"detail": "Item deleted successfully"}