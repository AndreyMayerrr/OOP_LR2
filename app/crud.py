from sqlalchemy.orm import Session
from datetime import datetime
from . import models, schemas


def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """Получает активные TodoList"""
    return db.query(models.TodoList) \
        .filter(models.TodoList.deleted_at.is_(None)) \
        .offset(skip) \
        .limit(limit) \
        .all()


def create_todo(db: Session, todo: schemas.TodoCreate):
    """Создание нового TodoList"""
    db_todo = models.TodoList(name=todo.name)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo_id: int, todo: schemas.TodoUpdate):
    """Обновление имени TodoList"""
    db_todo = db.query(models.TodoList).filter(models.TodoList.id == todo_id).first()
    if db_todo:
        db_todo.name = todo.name
        db.commit()
        db.refresh(db_todo)
    return db_todo


def delete_todo(db: Session, todo_id: int):
    """Логически удаляет TodoList, устанавливая deleted_at"""
    db_todo = db.query(models.TodoList).filter(models.TodoList.id == todo_id).first()
    if db_todo:
        db_todo.deleted_at = datetime.now()
        db.commit()


def mark_item_as_completed(db: Session, item_id: int):
    """Отмечает элемент как выполненный и обновляет статистику прогресса."""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db_item.is_done = True
        db.commit()

        # Получаем соответствующий TodoList и обновляем счётчики
        todo = db.query(models.TodoList).filter(models.TodoList.id == db_item.todo_id).first()
        if todo:
            todo.completed_count += 1
            db.commit()


def unmark_item_as_completed(db: Session, item_id: int):
    """Отменяет отметку выполнения элемента и обновляет статистику прогресса."""
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db_item.is_done = False
        db.commit()

        # Получаем соответствующий TodoList и обновляем счётчики
        todo = db.query(models.TodoList).filter(models.TodoList.id == db_item.todo_id).first()
        if todo:
            todo.completed_count -= 1
            db.commit()
