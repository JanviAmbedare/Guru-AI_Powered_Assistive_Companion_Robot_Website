from database.db_connection import get_connection


class TrainingService:

    @staticmethod
    def get_status(user_id: int):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        result = {}

        for job_type in ["face", "voice"]:

            cursor.execute("""
                SELECT *
                FROM model_training_queue
                WHERE user_id=%s
                AND type=%s
                ORDER BY id DESC
                LIMIT 1
            """,
            (
                user_id,
                job_type
            ))

            row = cursor.fetchone()

            if not row:

                result[f"{job_type}_status"] = "pending"
                result[f"{job_type}_progress"] = 0
                result[f"{job_type}_current_file"] = None
                result[f"{job_type}_total_files"] = 0
                result[f"{job_type}_processed_files"] = 0

            else:

                result[f"{job_type}_status"] = row["status"]
                result[f"{job_type}_progress"] = (
                    row["progress_percentage"] or 0
                )
                result[f"{job_type}_current_file"] = (
                    row["current_file"]
                )
                result[f"{job_type}_total_files"] = (
                    row["total_files"] or 0
                )
                result[f"{job_type}_processed_files"] = (
                    row["processed_files"] or 0
                )

        cursor.close()
        conn.close()

        return result