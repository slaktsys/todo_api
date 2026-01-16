from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class TodoPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class TodoBase(BaseModel):

    title: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Краткий заголовок задачи",
        examle=["Купить молоко"]
    )

    completed: bool = Field(
        default=False,
        description="Статус выполнения задачи"
    )

    priority: TodoPriority = Field(
        default=TodoPriority.MEDIUM,
        description="Приоритет задачи"
    )

    @field_validator("title")
    @classmethod
    def title_not_empty(cls, v:str) -> str:
        if not v.strip():
            raise ValueError("Заголовок не может быть пустым!")
        return v
    
class TodoCreate(TodoBase):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(
        None,
        min_lenght=1,
        max_lenght=255,
        description="Краткий заголовок задачи",
    )

    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Подробное описание задачи"
    )

    completed: Optional[bool] = Field(
        None,
        description="Статус выполнения задачи"
    )

    priority: Optional[TodoPriority] = Field(
        None,
        description="Приоритет задачи"
    )

class TodoResponse(TodoBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        from_attributes = True

class TodoListResponse(BaseModel):
    items: List[TodoResponse]
    total: int
    page: int
    size: int
    pages: int