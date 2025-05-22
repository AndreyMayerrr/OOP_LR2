from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class TodoList(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    completed_count = Column(Integer, nullable=False, default=0)  # Количество выполненных задач
    total_count = Column(Integer, nullable=False, default=0)      # Общее количество задач
    deleted_at = Column(DateTime, nullable=True)                  # Дата удаления (soft delete)

    items = relationship("Item", backref="todo", cascade="all,delete")  # Связь с элементами


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    text = Column(String)
    is_done = Column(Boolean, default=False)
    todo_id = Column(Integer, ForeignKey("todos.id"))              # Связь с ToDoList
    deleted_at = Column(DateTime, nullable=True)                  # Дата удаления (soft delete)
