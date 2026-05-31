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

        face_started = None
        face_completed = None

        voice_started = None
        voice_completed = None

        for row in rows:

            if row["type"] == "face":

                face_status = row["status"]
                face_started = row["started_at"]
                face_completed = row["completed_at"]

            elif row["type"] == "voice":

                voice_status = row["status"]
                voice_started = row["started_at"]
                voice_completed = row["completed_at"]

        cursor.close()
        conn.close()

        return {
            "face_status": face_status,
            "voice_status": voice_status,

            "face_started_at":
                face_started,

            "face_completed_at":
                face_completed,

            "voice_started_at":
                voice_started,

            "voice_completed_at":
                voice_completed
        }