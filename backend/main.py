from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.health import router as health_router
from backend.app.api.users import router as users_router
from backend.app.api.github import router as github_router
from backend.app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI-powered agentic software engineering platform",
    version=settings.app_version,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "DevNexa AI API is running",
        "version": settings.app_version,
        "environment": settings.environment,
    }


app.include_router(health_router)
app.include_router(users_router)
app.include_router(github_router)