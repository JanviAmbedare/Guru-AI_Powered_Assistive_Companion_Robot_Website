from fastapi import (
    APIRouter,
    UploadFile,
    File,
    HTTPException
)

import os
from models.schemas import UserCreate
from database.user_manager import UserManager
from database.biometric_manager import BiometricManager
from utils.auth import hash_password
from config.settings import settings
from services.logging_service import LoggingService

router = APIRouter(
    prefix="/register",
    tags=["Registration"]
)

user_mgr = UserManager()
bio_mgr = BiometricManager()

BASE_DIR = settings.BASE_STORAGE_PATH


@router.post("/user")
def register_user(data: UserCreate):

    hashed_password = hash_password(data.password)

    user_id = user_mgr.create_user(
        data.name,
        data.role,
        hashed_password,
        data.disability_type,
        data.language_pref
    )


    LoggingService.info(
        f"Registered user: {data.name}"
    )

    return {
        "status": "success",
        "user_id": user_id
    }

FACE_STORAGE = "backend/storage/faces"

@router.post("/face/{user_id}")
async def upload_face(
    user_id: int,
    files: list[UploadFile] = File(...)
):

    save_dir = os.path.join(
        FACE_STORAGE,
        str(user_id)
    )

    os.makedirs(save_dir, exist_ok=True)

    count = 0

    for file in files:

        file_path = os.path.join(
            save_dir,
            file.filename
        )

        with open(file_path, "wb") as f:

            f.write(await file.read())

        count += 1
    # Save biometric record for each uploaded face sample
    bio_mgr.save_biometric(
    user_id=user_id,
    bio_type="FACE",
    file_path=save_dir,
    sample_number=count,
    quality_score=95.0
        )
    return {
        "status": "success",
        "saved": count,
        "path": save_dir
    }


VOICE_STORAGE = "backend/storage/voices"


@router.post("/voice/{user_id}")
async def upload_voice(
    user_id: int,
    files: list[UploadFile] = File(...)
):

    save_dir = os.path.join(
        VOICE_STORAGE,
        str(user_id)
    )

    os.makedirs(save_dir, exist_ok=True)

    count = 0

    for file in files:

        file_path = os.path.join(
            save_dir,
            file.filename
        )

        with open(file_path, "wb") as f:

            f.write(await file.read())

        count += 1
    # Save biometric record for each uploaded voice sample
    bio_mgr.save_biometric(
    user_id=user_id,
    bio_type="VOICE",
    file_path=save_dir,
    sample_number=count,
    quality_score=92.0
        )


    return {
        "status": "success",
        "saved": count,
        "path": save_dir
    }