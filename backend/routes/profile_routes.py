from fastapi import APIRouter
from backend.models.schemas import ProfileCreate
from backend.database.profile_manager import UserProfileManager

router = APIRouter()


@router.post("/profile")
def create_profile(data: ProfileCreate):
    pm = UserProfileManager(data.user_id)
    pm.create_profile(data.name, data.preferences, data.health_info)
    return {"status": "Profile created"}


@router.get("/profile/{user_id}")
def get_profile(user_id: int):
    pm = UserProfileManager(user_id)
    return pm.get_profile()


@router.put("/profile/{user_id}")
def update_profile(user_id: int, data: ProfileCreate):
    pm = UserProfileManager(user_id)
    pm.update_profile(data.preferences, data.health_info)
    return {"status": "Profile updated"}


@router.delete("/profile/{user_id}")
def delete_profile(user_id: int):
    pm = UserProfileManager(user_id)
    pm.delete_profile()
    return {"status": "Profile deleted"}