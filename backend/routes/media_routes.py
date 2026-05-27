from flask import Blueprint
from flask import request
from flask import jsonify

from services.media_manager import MediaManager

media_bp = Blueprint(
    "media",
    __name__
)


# =========================
# FACE UPLOAD
# =========================

@media_bp.route(
    "/register/face/<int:user_id>",
    methods=["POST"]
)
def upload_face(user_id):

    try:

        files = request.files.getlist("files")

        uploaded_urls = (
            MediaManager.process_face_files(

            user_id=user_id,

            files=files,

            media_role=request.form.get(
                "media_role",
                "raw"
            )
        )
        )

        return jsonify({
            "status": "success",
            "uploaded": len(uploaded_urls),
            "urls": uploaded_urls
        })

    except Exception as e:

        print(e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500



# =========================
# VOICE UPLOAD
# =========================

@media_bp.route(
    "/register/voice/<int:user_id>",
    methods=["POST"]
)
def upload_voice(user_id):

    try:

        files = request.files.getlist("files")

        uploaded_urls = (
            MediaManager.process_voice_files(

            user_id=user_id,

            files=files,

            media_role=request.form.get(
                "media_role",
                "raw"
            )
        )
        )

        return jsonify({
            "status": "success",
            "uploaded": len(uploaded_urls),
            "urls": uploaded_urls
        })

    except Exception as e:

        print(e)

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500