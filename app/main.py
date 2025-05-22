from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from . import crud, models, schemas

app = FastAPI()

@app.get("/todos/", response_model=list[schemas.Todo])
def read_todos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Возвращает активный список TodoList'ов с расчетом прогресса"""
    todos = crud.get_todos(db, skip=skip, limit=limit)
    results = []
    for todo in todos:
        # Рассчитываем процент выполнения задач
        if todo.total_count > 0:
            progress = round((todo.completed_count / todo.total_count) * 100, 2)
        else:
            progress = 0.0
        results.append({
            "id": todo.id,
            "name": todo.name,
            "progress": progress
        })
    return results

@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
    """Создать новый TodoList"""
    return crud.create_todo(db=db, todo=todo)

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
    """Обновить название TodoList"""
    return crud.update_todo(db=db, todo_id=todo_id, todo=todo)

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Логически удалить TodoList"""
    crud.delete_todo(db=db, todo_id=todo_id)
    return {"detail": "Todo deleted successfully"}

@app.get("/todos/{todo_id}/items/", response_model=list[schemas.Item])
def read_items(todo_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Читает все активные элементы для выбранного TodoList"""
    items = db.query(models.Item)\
                .filter(models.Item.todo_id == todo_id, models.Item.deleted_at.is_(None))\
                .offset(skip)\
                .limit(limit)\
                .all()
    return items

@app.post("/todos/{todo_id}/items/", response_model=schemas.Item)
def create_item(todo_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """Создает новый элемент для выбранного TodoList"""
    return crud.create_item(db=db, item=item, todo_id=todo_id)

@app.put("/todos/{todo_id}/items/{item_id}")
def mark_item_as_completed(todo_id: int, item_id: int, db: Session = Depends(get_db)):
    """Отмечает элемент как выполненный и обновляет статистику прогресса"""
    crud.mark_item_as_completed(db=db, item_id=item_id)
    return {"detail": "Item marked as completed"}

@app.delete("/todos/{todo_id}/items/{item_id}")
def unmark_item_as_completed(todo_id: int, item_id: int, db: Session = Depends(get_db)):
    """Отменяет отметку выполнения элемента и обновляет статистику прогресса"""
    crud.unmark_item_as_completed(db=db, item_id=item_id)
    return {"detail": "Item unmarked as completed"}
