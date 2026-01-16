from contextlib import asynccontextmanager
from .database import create_tables
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from .core.config import settings
from .routers import todos_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Запуск приложения...")
    print("Создание таблиц в базе данных...")
    create_tables()
    print("Таблицы созданы!")
    yield

    print("Остановка приложения...")

app = FastAPI(
    title=settings.APP_NAME,
    description="Todo List",
    version=settings.APP_VERION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/", tags=["Корень"])
async def read_root():
    return {
        "message" : f"{settings.APP_NAME}",
        "version": settings.APP_VERION,
        "docs": "/docs",
        "redoc": "/redoc",
        "endpoints": {
            "todos": "/api/v1/todos"
        }
    }

@app.get("/health", tags=["Здоровье"])
async def health_check():
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERION
    }

app.include_router(todos_router)

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content = {
            "detail": "Endpoint не найден. Проверьте: /docs",
            "available_endpoints": [
                "GET /",
                "GET /health",
                "GET /docs",
                "GET /redoc",
                "GET /api/v1/todos",
                "POST /api/v1/todos",
                "GET /api/v1/todos/{id}",
                "PUT /api/v1/todos/{id}",
                "PATCH /api/v1/todos/{id}/complete",
                "DELETE /api/v1/todos/{id}",
            ]
        }
    )