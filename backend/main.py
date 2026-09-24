from fastapi import FastAPI

from backend.app.api.health import router as health_router

app = FastAPI(
    title="DevNexa AI API",
    description="AI-powered agentic software engineering platform",
    version="0.1.0",
)


@app.get("/")
def root():
    return {
        "message": "DevNexa AI API is running",
        "version": "0.1.0",
    }


app.include_router(health_router)
