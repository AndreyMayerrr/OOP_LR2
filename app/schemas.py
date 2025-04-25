# schemas.py
from pydantic import BaseModel
from typing import Optional, List

class TodoBase(BaseModel):

    name: str

class TodoCreate(TodoBase):

    pass

class TodoUpdate(TodoBase):

    name: Optional[str] = None  # добавляем возможность частичного обновления

class Todo(TodoBase):

    id: int

    class Config:
        from_attributes = True  # Позволяет преобразовывать объекты SQLAlchemy в модели Pydantic

class ItemBase(BaseModel):

    name: str
    text: str
    is_done: bool = False

class ItemCreate(ItemBase):

    pass

class ItemUpdate(ItemBase):

    name: Optional[str] = None
    text: Optional[str] = None
    is_done: Optional[bool] = None

class Item(ItemBase):

    id: int
    todo_id: int

    class Config:
        from_attributes = True
