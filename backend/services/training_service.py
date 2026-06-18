from database.db_connection import get_connection


class TrainingService:

    @staticmethod
    def get_status(user_id: int):

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT *
            FROM model_training_queue
            WHERE user_id=%s
            ORDER BY created_at DESC
        """, (user_id,))

        rows = cursor.fetchall()

        face_status = "pending"
        voice_status = "pending"

        face_progress = 0
        voice_progress = 0

        face_current_file = None
        voice_current_file = None

        face_total_files = 0
        voice_total_files = 0

        face_processed_files = 0
        voice_processed_files = 0

        for row in rows:

            if row["type"] == "face":

                face_status = row["status"]

                # face_started = row["started_at"]
                # face_completed = row["completed_at"]

                face_progress = (
                    row.get(
                        "progress_percentage",
                        0
                    ) or 0
                )

                face_current_file = (
                    row.get(
                        "current_file"
                    )
                )

                face_total_files = (
                    row.get(
                        "total_files",
                        0
                    ) or 0
                )

                face_processed_files = (
                    row.get(
                        "processed_files",
                        0
                    ) or 0
                )

            elif row["type"] == "voice":

                voice_status = row["status"]

                # voice_started = row["started_at"]
                # voice_completed = row["completed_at"]

                voice_progress = (
                    row.get(
                        "progress_percentage",
                        0
                    ) or 0
                )

                voice_current_file = (
                    row.get(
                        "current_file"
                    )
                )

                voice_total_files = (
                    row.get(
                        "total_files",
                        0
                    ) or 0
                )

                voice_processed_files = (
                    row.get(
                        "processed_files",
                        0
                    ) or 0
                )

        cursor.close()
        conn.close()

        return {

            "face_status": face_status,
            "voice_status": voice_status,

            "face_progress":
                face_progress,

            "voice_progress":
                voice_progress,

            "face_current_file":
                face_current_file,

            "voice_current_file":
                voice_current_file,

            "face_total_files":
                face_total_files,

            "voice_total_files":
                voice_total_files,

            "face_processed_files":
                face_processed_files,

            "voice_processed_files":
                voice_processed_files
        }