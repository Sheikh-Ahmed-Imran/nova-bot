from fastapi import FastAPI
from app.routes import hello, chatbot, health

app = FastAPI(title="FastAPI Test Setup")

# Include Routers
app.include_router(hello.router, prefix="", tags=["Hello"])
app.include_router(chatbot.router, prefix="/bot", tags=["Chatbot"])
app.include_router(health.router, prefix="/system", tags=["System"])

@app.get("/info")
def info():
    return {"project": "FastAPI production test", "version": "1.0"}
