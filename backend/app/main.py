from fastapi import FastAPI
from app.db import Base, engine
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Client-Deployed AI Agent Platform",
    version="1.0.0",
    description="Forward-deployed AI agent implementation platform.",
)

app.include_router(router)

@app.get("/health")
def health():
    return {"status": "ok", "service": "client-deployed-ai-agent-platform"}
