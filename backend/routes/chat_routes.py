from fastapi import APIRouter, Depends
from backend.models.schemas import ConversationCreate
from backend.services.ai_service import GuruAIService
from backend.utils.dependencies import get_current_user
from backend.services.logging_service import LoggingService

router = APIRouter(prefix="/chat", tags=["AI Chat"])


@router.post("/")
def chat(
    data: ConversationCreate,
    user=Depends(get_current_user)
):

    if user["user_id"] != data.user_id:
        return {
            "status": "error",
            "message": "Unauthorized"
        }

    result = GuruAIService.process_message(
        user_id=data.user_id,
        text=data.text
    )

    LoggingService.info(
        f"Chat message from user {data.user_id}"
    )

    return {
        "status": "success",
        "response": result["response"],
        "intent": result["intent"],
        "sentiment": result["sentiment"]
    }