from pydantic import BaseModel
from typing import Optional, List

class TodoBase(BaseModel):
    name: str

class TodoCreate(TodoBase):
    pass

class TodoUpdate(TodoBase):
    name: Optional[str] = None

class Todo(TodoBase):
    id: int
    progress: float  # Процент выполнения задач 

    class Config:
        from_attributes = True

class ItemBase(BaseModel):
    name: str
    text: str
    is_done: bool = False

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    todo_id: int

    class Config:
        from_attributes = True
