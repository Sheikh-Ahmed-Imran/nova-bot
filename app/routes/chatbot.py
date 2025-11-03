from fastapi import APIRouter, Body

router = APIRouter()

@router.post("/chat")
def chat_with_bot(user_message: str = Body(..., embed=True)):
    # For now, just echo message
    return {"reply": f"You said: {user_message}"}
