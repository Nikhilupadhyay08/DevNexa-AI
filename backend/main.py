from fastapi import FastAPI

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


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "devnexa-ai-backend",
    }
    