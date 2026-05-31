import os
import uuid

from dotenv import load_dotenv

from services.queue_service import QueueService
from services.cloudinary_service import (
    CloudinaryService
)

from database.db_connection import (
    get_connection as get_db_connection
)

load_dotenv()


class MediaManager:


    BASE_STORAGE = os.getenv(
        "GURU_STORAGE_PATH"
    )


    # =====================================
    # CREATE STORAGE DIRECTORY
    # =====================================

    @staticmethod
    def get_storage_path(
        media_category,
        media_role
    ):

        return os.path.join(

            MediaManager.BASE_STORAGE,

            media_category,

            media_role
        )


    # =====================================
    # SAVE LOCAL FILE
    # =====================================

    @staticmethod
    def save_local_file(
        file,
        media_category,
        media_role
    ):

        extension = (
            file.filename.split(".")[-1]
        )

        unique_name = (
            f"{uuid.uuid4()}.{extension}"
        )

        save_dir = (
            MediaManager.get_storage_path(
                media_category,
                media_role
            )
        )

        os.makedirs(
            save_dir,
            exist_ok=True
        )

        local_path = os.path.join(
            save_dir,
            unique_name
        )

        with open(local_path, "wb") as buffer:
            buffer.write(file.file.read())

        return (
            local_path,
            unique_name
        )


    # =====================================
    # CLOUDINARY UPLOAD
    # =====================================

    @staticmethod
    def upload_cloudinary(
        local_path,
        media_category
    ):

        folder = f"guru/{media_category}"

        resource_type = (
            "image"
            if media_category == "faces"
            else "video"
        )

        return CloudinaryService.upload_file(

            file_path=local_path,

            folder=folder,

            resource_type=resource_type
        )


    # =====================================
    # SAVE DATABASE RECORD
    # =====================================

    @staticmethod
    def save_media_record(data):

        connection = (
            get_db_connection()
        )

        cursor = connection.cursor()

        query = '''
        INSERT INTO media_files
        (
            user_id,
            media_category,
            media_role,
            file_name,
            local_path,
            cloudinary_url,
            public_id,
            file_size,
            mime_type,
            upload_source
        )
        VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''

        values = (

            data["user_id"],

            data["media_category"],

            data["media_role"],

            data["file_name"],

            data["local_path"],

            data["cloudinary_url"],

            data["public_id"],

            data["file_size"],

            data["mime_type"],

            data["upload_source"]
        )

        cursor.execute(
            query,
            values
        )

        connection.commit()

        cursor.close()
        connection.close()


    # =====================================
    # FACE FILE PROCESSOR
    # =====================================

    @staticmethod
    def process_face_files(
        user_id,
        files,
        media_role,
        upload_source="frontend"
    ):

        uploaded_files = []

        for file in files:

            # LOCAL SAVE
            local_path, file_name = (

                MediaManager.save_local_file(

                    file=file,

                    media_category="faces",

                    media_role=media_role
                )
            )

            # CLOUDINARY UPLOAD
            cloud_result = (

                MediaManager.upload_cloudinary(

                    local_path=local_path,

                    media_category="faces"
                )
            )

            # DATABASE RECORD
            MediaManager.save_media_record({

                "user_id": user_id,

                "media_category":
                    "faces",

                "media_role":
                    media_role,

                "file_name":
                    file_name,

                "local_path":
                    local_path,

                "cloudinary_url":
                    cloud_result["secure_url"],

                "public_id":
                    cloud_result["public_id"],

                "file_size":
                    os.path.getsize(
                        local_path
                    ),

                "mime_type":
                    file.mimetype,

                "upload_source":
                    upload_source
            })

            uploaded_files.append({

                "local_path":
                    local_path,

                "cloudinary_url":
                    cloud_result["secure_url"]
            })

            # Add face processing job to queue
            QueueService.add_job(
                user_id=user_id,
                job_type="face"
            )
        return uploaded_files


    # =====================================
    # VOICE FILE PROCESSOR
    # =====================================

    @staticmethod
    def process_voice_files(
        user_id,
        files,
        media_role,
        upload_source="frontend"
    ):

        uploaded_files = []

        for file in files:

            # LOCAL SAVE
            local_path, file_name = (

                MediaManager.save_local_file(

                    file=file,

                    media_category="voices",

                    media_role=media_role
                )
            )

            # CLOUDINARY UPLOAD
            cloud_result = (

                MediaManager.upload_cloudinary(

                    local_path=local_path,

                    media_category="voices"
                )
            )

            # DATABASE RECORD
            MediaManager.save_media_record({

                "user_id": user_id,

                "media_category":
                    "voices",

                "media_role":
                    media_role,

                "file_name":
                    file_name,

                "local_path":
                    local_path,

                "cloudinary_url":
                    cloud_result["secure_url"],

                "public_id":
                    cloud_result["public_id"],

                "file_size":
                    os.path.getsize(
                        local_path
                    ),

                "mime_type":
                    file.mimetype,

                "upload_source":
                    upload_source
            })

            uploaded_files.append({

                "local_path":
                    local_path,

                "cloudinary_url":
                    cloud_result["secure_url"]
            })

            # Add voice processing job to queue
            QueueService.add_job(
                user_id=user_id,
                job_type="voice"
            )

        return uploaded_files

    @staticmethod
    def get_media_status(user_id: int):

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                media_category,
                COUNT(*) as total
            FROM media_files
            WHERE user_id=%s
            AND is_active=1
            GROUP BY media_category
        """, (user_id,))

        rows = cursor.fetchall()

        face_count = 0
        voice_count = 0

        for row in rows:

            category = row["media_category"].lower()

            if category == "face":
                face_count = row["total"]

            elif category == "voice":
                voice_count = row["total"]

        cursor.close()
        conn.close()

        return {
            "face_uploaded": face_count > 0,
            "voice_uploaded": voice_count > 0,
            "face_count": face_count,
            "voice_count": voice_count
        }