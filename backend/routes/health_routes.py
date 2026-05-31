from fastapi import APIRouter
from pydantic import BaseModel

from services.ai_client import AIClient

router = APIRouter(
    tags=["Health"]
)

from services.emotion_service import EmotionService

router = APIRouter(
    prefix="/emotion",
    tags=["Emotion"]
)


@router.get("/latest/{user_id}")
def latest_emotion(user_id: int):

    return EmotionService.get_latest(
        user_id
    )
class HealthAnalysisRequest(
    BaseModel
):
    symptoms: str
    age: int | None = None


@router.get("/health")
def health_check():

    return {
        "status": "healthy",
        "service": "GURU Backend"
    }


@router.get("/history/{user_id}")
def emotion_history(user_id: int):

    return EmotionService.get_history(
        user_id
    )