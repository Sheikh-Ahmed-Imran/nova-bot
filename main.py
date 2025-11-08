from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from chatbot import create_client, detect_topic
from dotenv import load_dotenv
import os
import traceback

# Load env variables
load_dotenv()

app = FastAPI(title="Topic-Detection Chatbot API")

# ----------------------------
# CORS setup
# ----------------------------
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
        if not req.api_key:
            raise HTTPException(status_code=400, detail="API key is required")
        if not req.question:
            raise HTTPException(status_code=400, detail="Question is required")

        # Create client safely inside route
        client = create_client(req.api_key)
        category = detect_topic(req.question, client)

        return TopicResponse(category=category)

    except Exception as e:
        # Log full traceback for debugging
        traceback.print_exc()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Failed to detect topic",
                "exception": str(e)
            }
        )

# ----------------------------
# Test / health routes
# ----------------------------
@app.get("/")
def root():
    return {"message": "FastAPI backend is live!"}

@app.get("/mock_topic")
def mock_topic():
    # Simple test without Gemini API
    return {"mock": "This is a mock category"}

# ----------------------------
# Favicon route to avoid 500 logs
# ----------------------------

  # or just return an empty 204 if not available
