from fastapi import (
    APIRouter,
    HTTPException,
    UploadFile,
    File
)

from database.user_manager import UserManager
from utils.auth import (
    verify_password,
    create_access_token,
    hash_password
)

from services.ai_client import AIClient
from services.logging_service import LoggingService
from models.schemas import LoginRequest, UserCreate

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

user_mgr = UserManager()


@router.post("/login")
def login(data: LoginRequest):

    user = user_mgr.get_user_by_name(data.name)

    if not user:
        raise HTTPException(401, "User not found")

    if not verify_password(
        data.password,
        user["password"]
    ):
        raise HTTPException(401, "Invalid password")

    token = create_access_token({
        "user_id": user["id"],
        "role": user["role"]
    })

    return {
        "status": "success",
        "access_token": token,
        "user_id": user["id"],
        "role": user["role"]
    }


@router.post("/face-login")
async def face_login(
    file: UploadFile = File(...)
):

    result = AIClient.verify_face(file)

    if not result.get("verified"):
        raise HTTPException(
            401,
            "Face verification failed"
        )

    user_id = result["user_id"]

    user = user_mgr.get_user_by_id(user_id)

    token = create_access_token({
        "user_id": user["id"],
        "role": user["role"]
    })

    return {
        "status": "success",
        "access_token": token,
        "user_id": user["id"],
        "role": user["role"]
    }


@router.post("/voice-login")
async def voice_login(
    file: UploadFile = File(...)
):

    result = AIClient.verify_voice(file)

    if not result.get("verified"):
        raise HTTPException(
            401,
            "Voice verification failed"
        )

    user_id = result["user_id"]

    user = user_mgr.get_user_by_id(user_id)

    token = create_access_token({
        "user_id": user["id"],
        "role": user["role"]
    })

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