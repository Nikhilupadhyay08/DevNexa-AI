from fastapi import FastAPI

from backend.app.api.health import router as health_router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI-powered agentic software engineering platform",
    version=settings.app_version,
)


@app.get("/")
def root():
    return {
        "message": "DevNexa AI API is running",
        "version": settings.app_version,
        "environment": settings.environment,
    }


app.include_router(health_router)
