from fastapi import APIRouter
from sqlalchemy import text

from database.db_connection import *

from services.queue_service import QueueService
from services.training_service import TrainingService

router = APIRouter(
    tags=["Training"]
)


@router.get("/training/status/{user_id}")
def get_training_status(user_id:int):

    return TrainingService.get_status(
        user_id
    )


@router.post("/training/retrain/{user_id}")
def retrain_user(user_id:int):

    db = get_connection()

    try:

        face_count = db.execute(
            text("""
                SELECT COUNT(*)
                FROM media_files
                WHERE user_id=:user_id
                AND media_category='faces'
                AND is_active=1
            """),
            {"user_id": user_id}
        ).scalar()

        voice_count = db.execute(
            text("""
                SELECT COUNT(*)
                FROM media_files
                WHERE user_id=:user_id
                AND media_category='voices'
                AND is_active=1
            """),
            {"user_id": user_id}
        ).scalar()

        QueueService.force_retrain(
            user_id,
            "face",
            face_count
        )

        QueueService.force_retrain(
            user_id,
            "voice",
            voice_count
        )

        return {
            "status":"success",
            "message":"Retraining queued"
        }

    finally:
        db.close()