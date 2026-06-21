from fastapi import APIRouter

from database.db_connection import get_connection

from services.queue_service import QueueService
from services.training_service import TrainingService

router = APIRouter(
    tags=["Training"]
)


@router.get("/training/status/{user_id}")
def get_training_status(user_id: int):

    return TrainingService.get_status(
        user_id
    )


@router.post("/training/retrain/{user_id}")
def retrain_user(user_id: int):

    conn = get_connection()
    cursor = conn.cursor()

    try:

        cursor.execute("""
            SELECT COUNT(*)
            FROM media_files
            WHERE user_id=%s
            AND media_category='faces'
            AND is_active=1
        """, (user_id,))

        face_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT COUNT(*)
            FROM media_files
            WHERE user_id=%s
            AND media_category='voices'
            AND is_active=1
        """, (user_id,))

        voice_count = cursor.fetchone()[0]

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
            "status": "success",
            "message": "Retraining queued",
            "face_files": face_count,
            "voice_files": voice_count
        }

    finally:

        cursor.close()
        conn.close()