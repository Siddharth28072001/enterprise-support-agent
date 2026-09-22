from fastapi import FastAPI
from sqlalchemy import text

from app.config import settings
from app.database import engine

from app.api.documents import router as documents_router

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)

app.include_router(documents_router)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.app_env,
    }


@app.get("/health/db")
def database_health_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        return {
            "database": "healthy",
            "result": result.scalar(),
        }