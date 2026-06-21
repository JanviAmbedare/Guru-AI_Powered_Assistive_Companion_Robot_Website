import uuid

from dotenv import load_dotenv

from services.queue_service import QueueService
from services.cloudinary_service import (
    CloudinaryService
)
import cloudinary.uploader
from database.db_connection import (
    get_connection as get_db_connection
)

load_dotenv()


class MediaManager:


    # # =====================================
    # # CREATE STORAGE DIRECTORY
    # # =====================================

    # @staticmethod
    # def get_storage_path(
    #     media_category,
    #     media_role
    # ):

    #     return os.path.join(

    #         MediaManager.BASE_STORAGE,

    #         media_category,

    #         media_role
    #     )


    # # =====================================
    # # SAVE LOCAL FILE
    # # =====================================

    # @staticmethod
    # def save_local_file(
    #     file,
    #     media_category,
    #     media_role
    # ):

    #     extension = (
    #         file.filename.split(".")[-1]
    #     )

    #     unique_name = (
    #         f"{uuid.uuid4()}.{extension}"
    #     )

    #     save_dir = (
    #         MediaManager.get_storage_path(
    #             media_category,
    #             media_role
    #         )
    #     )

    #     os.makedirs(
    #         save_dir,
    #         exist_ok=True
    #     )

    #     local_path = os.path.join(
    #         save_dir,
    #         unique_name
    #     )

    #     with open(local_path, "wb") as buffer:
    #         buffer.write(file.file.read())

    #     return (
    #         local_path,
    #         unique_name
    #     )


    # # =====================================
    # # CLOUDINARY UPLOAD
    # # =====================================

    # @staticmethod
    # def upload_cloudinary(
    #     local_path,
    #     media_category
    # ):

    #     folder = f"guru/{media_category}"

    #     resource_type = (
    #         "image"
    #         if media_category == "faces"
    #         else "video"
    #     )

    #     return CloudinaryService.upload_file(

    #         file_path=local_path,

    #         folder=folder,

    #         resource_type=resource_type
    #     )


    # =====================================
    # SAVE DATABASE RECORD
    # =====================================

    @staticmethod
    def save_media_record(data):
        print("SAVING MEDIA RECORD TO DB")
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
        print("EXECUTING QUERY:")
        cursor.execute(
            query,
            values
        )
        print("QUERY EXECUTED, COMMITTING")
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
        print("PROCESS FACE FILES START")
        uploaded_files = []

        QueueService.add_job(
            user_id=user_id,
            job_type="face",
            total_files=len(files)
        )

        processed = 0
        print("FILES RECEIVED =", len(files))
        for file in files:

            cloud_result = (
                CloudinaryService.upload_file(
                    file=file,
                    folder="guru/faces",
                    resource_type="image"
                )
            )
            print("CLOUDINARY URL =", cloud_result["secure_url"])
            MediaManager.save_media_record({

                "user_id": user_id,

                "media_category":
                    "faces",

                "media_role":
                    media_role,

                "file_name":
                    file.filename,

                "local_path":
                    None,

                "cloudinary_url":
                    cloud_result["secure_url"],

                "public_id":
                    cloud_result["public_id"],

                "file_size":
                    0,

                "mime_type":
                    file.content_type,

                "upload_source":
                    upload_source
            })

            uploaded_files.append({

                "cloudinary_url":
                    cloud_result["secure_url"],

                "public_id":
                    cloud_result["public_id"]
            })
            print("UPLOADED FILE =", uploaded_files[-1])
            processed += 1

            QueueService.update_progress(

                user_id=user_id,

                job_type="face",

                current_file=file.filename,

                processed_files=processed
            )
        QueueService.mark_completed(
            user_id=user_id,
            job_type="face"
        )
        print("PROCESS FACE FILES END")
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
        print("PROCESS VOICE FILES START")
        uploaded_files = []

        QueueService.add_job(

            user_id=user_id,

            job_type="voice",

            total_files=len(files)
        )

        processed = 0

        for file in files:

            print("=" * 50)
            print("VOICE FILE:", file.filename)
            print("TYPE:", type(file))
            print("CONTENT:", file.content_type)
            print("=" * 50)

            cloud_result = (
                CloudinaryService.upload_file(
                    file=file,
                    folder="guru/voices",
                    resource_type="video"
                )
            )
            print("CLOUDINARY URL =", cloud_result["secure_url"])

            print("INSERTING DB RECORD")
            MediaManager.save_media_record({

                "user_id": user_id,

                "media_category":
                    "voices",

                "media_role":
                    media_role,

                "file_name":
                    file.filename,

                "local_path":
                    None,

                "cloudinary_url":
                    cloud_result["secure_url"],

                "public_id":
                    cloud_result["public_id"],

                "file_size":
                    0,

                "mime_type":
                    file.content_type,

                "upload_source":
                    upload_source
            })

            uploaded_files.append({

                "cloudinary_url":
                    cloud_result["secure_url"],

                "public_id":
                    cloud_result["public_id"]
            })

            processed += 1

            QueueService.update_progress(

                user_id=user_id,

                job_type="voice",

                current_file=file.filename,

                processed_files=processed
            )

        QueueService.mark_completed(
            user_id=user_id,
            job_type="voice"
        )
        print("PROCESS VOICE FILES END")
        return uploaded_files

    @staticmethod
    def get_media_status(user_id: int):

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT

            media_category,

            COUNT(*) as total,

            SUM(
                CASE
                    WHEN cloudinary_url IS NOT NULL
                    THEN 1
                    ELSE 0
                END
            ) as uploaded_count,

            SUM(
                CASE
                    WHEN is_processed=1
                    THEN 1
                    ELSE 0
                END
            ) as processed_count,

            SUM(
                CASE
                    WHEN is_used_for_training=1
                    THEN 1
                    ELSE 0
                END
            ) as trained_count

        FROM media_files

        WHERE user_id=%s
        AND is_active=1

        GROUP BY media_category
        """, (user_id,))

        rows = cursor.fetchall()

        face_total = 0
        face_uploaded = 0
        face_processed = 0
        face_training = 0

        voice_total = 0
        voice_uploaded = 0
        voice_processed = 0
        voice_training = 0
        
        print("ROWS =", rows)
        
        for row in rows:

            category = row["media_category"].lower()

            if category == "faces":

                face_total = row["total"]

                face_uploaded = (
                    row["uploaded_count"] or 0
                )

                face_processed = (
                    row["processed_count"] or 0
                )

                face_training = (
                    row["trained_count"] or 0
                )

            elif category == "voices":

                voice_total = row["total"]

                voice_uploaded = (
                    row["uploaded_count"] or 0
                )

                voice_processed = (
                    row["processed_count"] or 0
                )

                voice_training = (
                    row["trained_count"] or 0
                )

        cursor.close()
        conn.close()

        return {

                "face":{

                    "total": face_total,

                    "uploaded":
                        face_uploaded,

                    "processed":
                        face_processed,

                    "training":
                        face_training
                },

                "voice":{

                    "total": voice_total,

                    "uploaded":
                        voice_uploaded,

                    "processed":
                        voice_processed,

                    "training":
                        voice_training
                }
            }
    @staticmethod
    def clear_user_media(user_id: int):

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT public_id,
                media_category
            FROM media_files
            WHERE user_id=%s
        """, (user_id,))

        files = cursor.fetchall()

        for file in files:

            try:

                if file["public_id"]:

                    if file["media_category"] == "voices":

                        cloudinary.uploader.destroy(
                            file["public_id"],
                            resource_type="video"
                        )

                    else:

                        cloudinary.uploader.destroy(
                            file["public_id"]
                        )

            except Exception as e:

                print(
                    f"Cloudinary delete error: {e}"
                )

        cursor.execute("""
            DELETE FROM media_files
            WHERE user_id=%s
        """, (user_id,))
        # delete from model_training_queue and biometric_profiles tables for the user
        cursor.execute("""
            DELETE FROM model_training_queue
            WHERE user_id=%s
        """, (user_id,))

        # 
        cursor.execute("""
            DELETE FROM biometric_profiles
            WHERE user_id=%s
        """, (user_id,))
        conn.commit()

        cursor.close()
        conn.close()

        return True