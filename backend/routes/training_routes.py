from fastapi import APIRouter
from services.training_service import (
    TrainingService
)

router = APIRouter(
    tags=["Training"]
)

@router.get("/training/status/{user_id}")
def get_training_status(
    user_id: int
):

    return TrainingService.get_status(
        user_id
    )