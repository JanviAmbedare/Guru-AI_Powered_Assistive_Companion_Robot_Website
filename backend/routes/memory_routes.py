from fastapi import APIRouter, HTTPException
from flask import Blueprint, jsonify, request
from models.schemas import ProfileCreate
from database.profile_manager import UserProfileManager
from database.db_utils import execute_query
from database.memory_manager import MemoryManager
from services.context_memory_service import ContextMemoryService
from services.daily_summary_service import DailySummaryService
from services.emotion_service import EmotionPredictionService
router = APIRouter()

memory_bp = Blueprint(
    "memory_bp",
    __name__
)

@router.post("/")
def create_profile(data: ProfileCreate):
    try:
        pm = UserProfileManager(data.user_id)
        pm.create_profile(data.name, data.preferences, data.health_info)
        return {"status": "Profile created"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}")
def get_profile(user_id: int):
    try:
        pm = UserProfileManager(user_id)
        return pm.get_profile()

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}")
def update_profile(user_id: int, data: ProfileCreate):
    try:
        pm = UserProfileManager(user_id)
        pm.update_profile(data.preferences, data.health_info)
        return {"status": "Profile updated"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}")
def delete_profile(user_id: int):
    try:
        pm = UserProfileManager(user_id)
        pm.delete_profile()
        return {"status": "Profile deleted"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ---------------------------------------------------
# GET MEMORIES
# ---------------------------------------------------

@memory_bp.route("/api/memory/<int:user_id>")
def get_memories(user_id):

    mm = MemoryManager(user_id)

    data = mm.get_recent_context(50)

    return jsonify(data)

# ---------------------------------------------------
# SEARCH MEMORIES
# ---------------------------------------------------

@memory_bp.route("/api/memory/search/<int:user_id>")
def search_memories(user_id):

    q = request.args.get("q")

    results = (
        ContextMemoryService
        .search_similar_memories(
            user_id,
            q
        )
    )

    return jsonify(results)

# ---------------------------------------------------
# DAILY SUMMARY
# ---------------------------------------------------

@memory_bp.route("/api/memory/daily-summary/<int:user_id>")
def daily_summary(user_id):

    data = (
        DailySummaryService
        .generate_summary(user_id)
    )

    return jsonify(data)

# ---------------------------------------------------
# EMOTION PREDICTION
# ---------------------------------------------------

@memory_bp.route("/api/memory/emotion-predict/<int:user_id>")
def emotion_predict(user_id):

    data = (
        EmotionPredictionService
        .predict(user_id)
    )

    return jsonify(data)