from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoListResponse, TodoResponse, TodoUpdate


router = APIRouter(
    prefix="/api/v1/todos",
    tags=["todos"],
    responses={
        404: {"description": "Не найдено"},
        400: {"description": "Неверный запрос"}
    }
)

@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую задачу",
    description="Создает новую задачу с указанными параметрами"
)
async def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db) 
):
    try:
        todo_data = todo.model_dump()
        if "priority" in todo_data and hasattr(todo_data["priority"], "value"):
            todo_data["priority"] = todo_data["priority"].value

        db_todo = Todo(**todo_data)
        db.add(db_todo)
        db.commit()
        db.refresh(db_todo)
        return db_todo
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании задачи: {str(e)}"
        )

@router.get(
    "/",
    response_model=TodoListResponse,
    summary="Получить список задач",
    description="Возращает список задач с пагинацией и фильтрацией"
)
async def read_todos(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1, description="Номер страницы"),
    size: int = Query(10, ge=1, le=100, description="Размер страницы"),
    completed: Optional[bool] = Query(None, description= "Фильтр по статусу"),
    priority: Optional[str] = Query(None, description= "Фильтр по приоритету")
):
    query = db.query(Todo)
    if completed is not None:
        query = query.filter(Todo.completed == completed)
    
    if priority is not None:
        query = query.filter(Todo.priority  == priority)

    total = query.count()
    items = query.offset((page-1)*size).limit(size).all()
    pages = (total+size-1)//size

    return TodoListResponse(
        items=items,
        total=total,
        page=page,
        size=size,
        pages=pages
    )

@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Полностью обновить задачу",
    description="Обновляет все поля задачи"
)
async def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db)
):

    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {todo_id} не найдена"
        )

    update_data = todo_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(todo, field, value)

    db.flush()
    db.refresh(todo)
    db.commit()
    
    return todo

@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    summary="Получить задачу по ID",
    description="Возвращает задачу по указанному идентификатору"
)
async def read_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    todo = db.query(Todo).filter(Todo.id == todo_id).first()

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с ID {todo_id} не найдена"
        )

    return todo

@router.patch(
    "/{todo_id}/complete",
    response_model=TodoResponse,
    summary="Отметить задачу как выполненную",
    description="Изменяет статус задачи на 'выполнено'"
)
async def complete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача с ID {todo_id} не найдена"
            )
        
        todo.completed = True

        db.flush()
        db.refresh(todo)
        db.commit()

        return todo
    
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при обновлении задачи: {str(e)}"
        )

@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу",
    description="Удаляет задачу по указанному идентификатору"
)
async def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db)
):
    try:
        todo = db.query(Todo).filter(Todo.id == todo_id).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Задача с ID {todo_id} не найдена"
            )
        
        db.delete(todo)
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении задачи: {str(e)}"
        )