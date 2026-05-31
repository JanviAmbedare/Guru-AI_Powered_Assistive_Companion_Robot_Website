from fastapi import APIRouter, Depends
from models.schemas import ChatRequest
from utils.dependencies import get_current_user

from services.ai_client import AIClient
from services.logging_service import LoggingService

router = APIRouter(
    prefix="/chat",
    tags=["AI Chat"]
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

    result = AIClient.chat(
        user_id=data.user_id,
        message=data.text
    )

    LoggingService.info(
        f"Chat message from user {data.user_id}"
    )

    return {
        "status": "success",
        "response": result.get(
            "response",
            ""
        ),
        "intent": result.get(
            "intent",
            "unknown"
        ),
        "sentiment": result.get(
            "sentiment",
            "neutral"
        )
    }