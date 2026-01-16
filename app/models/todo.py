import enum
from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String, Text
from sqlalchemy.sql import func
from app.database import Base

class TodoPriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Todo(Base):
    __tablename__ = "todos"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
        comment="Уникальный идентификатор"
    )

    title = Column(
        String(255),
        index=True,
        nullable=False,
        comment="Заголовок задачи"
    )

    description = Column(
        Text,
        nullable=True,
        comment="Подробное описание задачи"
    )

    completed = Column(
        Boolean,
        default=False,
        comment="Статус выполнения задачи"
    )

    priority = Column(
        Enum(TodoPriorityEnum),
        default=TodoPriorityEnum.MEDIUM,
        nullable=False,
        comment="Приоритет задачи"
    )

    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        comment="Дата и время создания"
    )

    updated_at = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
        comment="Дата и время последнего обновления"
    )

    def __repr__(self):
        return f"<Todo(id={self.id}, title={self.title}, comleted={self.completed})>"