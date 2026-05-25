from fastapi import APIRouter, HTTPException
from backend.database.user_manager import UserManager
from backend.models.schemas import LoginRequest, UserCreate
from backend.utils.auth import (
    verify_password,
    create_access_token,
    hash_password
)
from backend.services.logging_service import LoggingService

router = APIRouter(prefix="/auth",tags=["Authentication"])

user_mgr = UserManager()


@router.post("/login")
def login(data: LoginRequest):

    user = user_mgr.get_user_by_name(data.name)

    if not user:
        raise HTTPException(401, "User not found")

    if not verify_password(data.password, user["password"]):
        raise HTTPException(401, "Invalid password")

    token = create_access_token({
        "user_id": user["id"],
        "role": user["role"]
    })

    LoggingService.info(
        f"User logged in: {user['name']}"
    )

    return {
        "status": "success",
        "access_token": token,
        "user_id": user["id"],
        "role": user["role"]
    }


@router.post("/register")
def register(data: UserCreate):

    hashed_password = hash_password(data.password)

    user_id = user_mgr.create_user(
        data.name,
        data.role,
        hashed_password,
        data.disability_type,
        data.language_pref
    )

    LoggingService.info(
        f"New user registered: {data.name}"
    )

    return {
        "status": "success",
        "user_id": user_id
    }