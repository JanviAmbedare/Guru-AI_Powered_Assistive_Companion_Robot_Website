from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Form
from fastapi import HTTPException

from typing import List

from services.media_manager import MediaManager
import traceback

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
    print("FACE ROUTE HIT")
    print("FILES RECEIVED =", len(files))
    try:

        uploaded_urls = (
            MediaManager.process_face_files(
                user_id=user_id,
                files=files,
                media_role=media_role
            )
        )
        # print("CLOUDINARY URL =", uploaded_urls[0] if uploaded_urls else None)
        return {
            "status": "success",
            "uploaded": len(uploaded_urls),
            "urls": uploaded_urls
        }

    except Exception as e:

        traceback.print_exc()
        
        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# VOICE UPLOAD
# =========================

@router.post("/register/voice/{user_id}")
async def upload_voice(
    user_id: int,
    files: List[UploadFile] = File(...),
    media_role: str = Form("raw")
):
    print("VOICE ROUTE HIT")
    print("FILES RECEIVED =", len(files))
    try:

        uploaded_urls = (
            MediaManager.process_voice_files(
                user_id=user_id,
                files=files,
                media_role=media_role
            )
        )
        # print("CLOUDINARY URL =", cloudinary_url)

        return {
            "status": "success",
            "uploaded": len(uploaded_urls),
            "urls": uploaded_urls
        }

    except Exception as e:

        print(e)

        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/status/{user_id}")
def media_status(user_id: int):

    media = MediaManager.get_media_status(
        user_id
    )
    print("MEDIA STATUS =", media)
    
    return {

        "face_uploaded":
            media["face"]["uploaded"] > 0,

        "voice_uploaded":
            media["voice"]["uploaded"] > 0,

        "face_count":
            media["face"]["total"],

        "voice_count":
            media["voice"]["total"],

        "face":
            media["face"],

        "voice":
            media["voice"]
    }

@router.delete("/media/user/{user_id}")
def clear_user_media(user_id: int):

    MediaManager.clear_user_media(user_id)

    return {
        "status": "success",
        "message": "Old media removed"
    }