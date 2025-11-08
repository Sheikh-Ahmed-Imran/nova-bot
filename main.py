from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import create_client, detect_topic
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="Topic-Detection Chatbot API")

# Allow requests from frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print(f"[Debug] FRONTEND_URL={FRONTEND_URL}")

# ----------------------------
# Models
# ----------------------------
class TopicRequest(BaseModel):
    api_key: str
    question: str

class TopicResponse(BaseModel):
    category: str

# ----------------------------
# Main route
# ----------------------------
@app.post("/detect_topic", response_model=TopicResponse)               
def detect_topic_route(req: TopicRequest):
    try:
        client = create_client(req.api_key)
        category = detect_topic(req.question, client)
        return TopicResponse(category=category)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ----------------------------
# ✅ Test routes
# ----------------------------
@app.get("/")
def root():
    return {"message": "FastAPI backend is live!"}


@app.get("/mock_topic")
def mock_topic():
    # Simple test without API key
    return {"mock": "This is mock category"}
