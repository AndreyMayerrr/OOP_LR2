# crud.py
from sqlalchemy.orm import Session
from . import models, schemas

def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """
    Получает список всех TodoList'ов, применяя ограничения по пропускаемым и максимальному количеству записей.
    """
    return db.query(models.Todo).offset(skip).limit(limit).all()

def create_todo(db: Session, todo: schemas.TodoCreate):
    """
    Создает новый TodoList в базе данных.
    """
    db_todo = models.Todo(name=todo.name)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    """
    Обновляет существующие данные TodoList по его идентификатору.
    """
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db_todo.name = todo.name
        db.commit()
        db.refresh(db_todo)
    return db_todo

def delete_todo(db: Session, todo_id: int):
    """
    Удаляет TodoList по его идентификатору.
    """
    db_todo = db.query(models.Todo).filter(models.Todo.id == todo_id).first()
    if db_todo:
        db.delete(db_todo)
        db.commit()

def get_items(db: Session, todo_id: int, skip: int = 0, limit: int = 100):
    """
    Получает список всех элементов (Items) для указанного TodoList.
    """
    return db.query(models.Item).filter(models.Item.todo_id == todo_id).offset(skip).limit(limit).all()

def create_item(db: Session, item: schemas.ItemCreate, todo_id: int):
    """
    Создает новый элемент (Item) в указанном TodoList.
    """
    db_item = models.Item(**item.model_dump(), todo_id=todo_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def update_item(db: Session, item_id: int, item: schemas.ItemUpdate):
    """
    Обновляет данные элемента (Item) по его идентификатору.
    """
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db_item.name = item.name
        db_item.text = item.text
        db_item.is_done = item.is_done
        db.commit()
        db.refresh(db_item)
    return db_item

def delete_item(db: Session, item_id: int):
    """
    Удаляет элемент (Item) по его идентификатору.
    """
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()