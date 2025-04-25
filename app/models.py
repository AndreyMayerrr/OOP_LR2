# models.py
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Todo(Base):
    """
    Класс модели TodoList, представляет таблицу в базе данных.
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    # Связь один ко многим между Todo и Item
    items = relationship("Item", backref="todo", cascade="all,delete")

class Item(Base):
    """
    Класс модели Item, представляющий элементы списка дел.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    text = Column(String)
    is_done = Column(Boolean, default=False)

    # Внешний ключ на родительский TodoList
    todo_id = Column(Integer, ForeignKey("todos.id"))