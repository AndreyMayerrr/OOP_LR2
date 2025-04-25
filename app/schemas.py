# schemas.py
from pydantic import BaseModel
from typing import Optional, List

class TodoBase(BaseModel):
    """
    Базовая структура данных для TodoList.
    """
    name: str

class TodoCreate(TodoBase):
    """
    Валидная структура для создания новых TodoList.
    """
    pass

class TodoUpdate(TodoBase):
    """
    Валидная структура для обновления существующих TodoList.
    """
    name: Optional[str] = None  # добавляем возможность частичного обновления

class Todo(TodoBase):
    """
    Структура, включающая дополнительный атрибут id, полученный из базы данных.
    """
    id: int

    class Config:
        from_attributes = True  # Позволяет преобразовывать объекты SQLAlchemy в модели Pydantic

class ItemBase(BaseModel):
    """
    Базовая структура данных для элементов (Items).
    """
    name: str
    text: str
    is_done: bool = False

class ItemCreate(ItemBase):
    """
    Валидная структура для создания новых элементов.
    """
    pass

class ItemUpdate(ItemBase):
    """
    Валидная структура для обновления существующих элементов.
    """
    name: Optional[str] = None
    text: Optional[str] = None
    is_done: Optional[bool] = None

class Item(ItemBase):
    """
    Структура, включающая внешний ключ и id.
    """
    id: int
    todo_id: int

    class Config:
        from_attributes = True