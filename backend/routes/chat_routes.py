from fastapi import APIRouter, Depends
from models.schemas import ChatRequest
from utils.dependencies import get_current_user
from services.logging_service import LoggingService

import requests

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
)

AI_SERVICE_URL = (
    "https://guru-ai-service.onrender.com/chat"
)

@router.post("/")
def chat(
    data: ChatRequest,
    user=Depends(get_current_user)
):

    if user["user_id"] != data.user_id:

        return {
            "status": "error",
            "message": "Unauthorized"
        }

    response = requests.post(
        AI_SERVICE_URL,
        json={
            "user_id": data.user_id,
            "message": data.text
        }
    )

    result = response.json()

    LoggingService.info(
        f"Chat message from user {data.user_id}"
    )

    return {
        "status": "success",
        "response": result["response"],
        "intent": result["intent"],
        "sentiment": result["sentiment"]
    }