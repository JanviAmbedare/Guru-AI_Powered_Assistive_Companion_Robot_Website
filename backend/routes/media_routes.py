from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import HTTPException

from typing import List

from services.media_manager import MediaManager


router = APIRouter()


# =========================
# FACE UPLOAD
# =========================

@router.post("/register/face/{user_id}")
async def upload_face(
    user_id: int,
    files: List[UploadFile] = File(...),
    media_role: str = Form("raw")
):

    try:

        uploaded_urls = (
            MediaManager.process_face_files(
                user_id=user_id,
                files=files,
                media_role=media_role
            )
        )

        return {
            "status": "success",
            "uploaded": len(uploaded_urls),
            "urls": uploaded_urls
        }

    except Exception as e:

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# =========================
# VOICE UPLOAD
# =========================

@router.post("/register/voice/{user_id}")
async def upload_voice(
    user_id: int,
    files: List[UploadFile] = File(...),
    media_role: str = Form("raw")
):

    try:

        uploaded_urls = (
            MediaManager.process_voice_files(
                user_id=user_id,
                files=files,
                media_role=media_role
            )
        )

        return {
            "status": "success",
            "uploaded": len(uploaded_urls),
            "urls": uploaded_urls
        }

    except Exception as e:

        print(e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )