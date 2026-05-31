from fastapi import APIRouter

from models.schemas import ProfileCreate
from database.profile_manager import UserProfileManager
from services.ai_client import AIClient

router = APIRouter()


@router.post("/profile")
def create_profile(data: ProfileCreate):

    pm = UserProfileManager(data.user_id)

    pm.create_profile(
        data.name,
        data.preferences,
        data.health_info
    )

    return {"status": "Profile created"}


@router.get("/profile/{user_id}")
def get_profile(user_id: int):

    pm = UserProfileManager(user_id)

    return pm.get_profile()


@router.put("/profile/{user_id}")
def update_profile(
    user_id: int,
    data: ProfileCreate
):

    pm = UserProfileManager(user_id)

    pm.update_profile(
        data.preferences,
        data.health_info
    )

    return {
        "status": "Profile updated"
    }


@router.post("/profile/{user_id}/retrain")
def retrain_models(user_id: int):

    face_result = AIClient.train_face(user_id)

    voice_result = AIClient.train_voice(user_id)

    return {
        "status": "success",
        "face": face_result,
        "voice": voice_result
    }

@router.delete("/profile/{user_id}")
def delete_profile(user_id: int):
    pm = UserProfileManager(user_id)
    pm.delete_profile()
    return {"status": "Profile deleted"}