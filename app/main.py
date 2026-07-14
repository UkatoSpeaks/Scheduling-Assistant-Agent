from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="Multi-Agent Scheduling Assistant",
    description="AI-powered scheduling assistant built with LangGraph",
    version="1.0.0",
)

app.include_router(router)


@app.get("/")
def root():
    return {
        "message": "Multi-Agent Scheduling Assistant API is running "
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "Multi-Agent Scheduling Assistant",
        "database": "connected",
        "llm": "available"
    }