from database.db_connection import get_connection
class QueueService:

    @staticmethod
    def add_job(
        user_id,
        job_type,
        total_files
    ):

        conn = get_connection()
        cursor = conn.cursor()

        # Check if active job already exists

        cursor.execute(
            """
            SELECT id
            FROM model_training_queue
            WHERE user_id=%s
            AND type=%s
            AND status IN
            (
                'pending',
                'uploading',
                'training'
            )
            LIMIT 1
            """,
            (
                user_id,
                job_type
            )
        )

        existing_job = cursor.fetchone()

        if existing_job:

            cursor.close()
            conn.close()

            return {
                "status": "exists",
                "message":
                    f"{job_type} job already active"
            }
        
        cursor.execute(
            """
            INSERT INTO model_training_queue
            (
                user_id,
                type,
                status,
                total_files,
                processed_files,
                progress_percentage
            )
            VALUES
            (
                %s,
                %s,
                'uploading',
                %s,
                0,
                0
            )
                        """,
            (
                user_id,
                job_type,
                total_files
            )
        )

        conn.commit()

        cursor.close()
        conn.close()
        
    @staticmethod
    def update_progress(
        user_id,
        job_type,
        processed_files,
        current_file
    ):
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT total_files
            FROM model_training_queue
            WHERE user_id=%s
            AND type=%s
            ORDER BY id DESC
            LIMIT 1
            """,
            (
                user_id,
                job_type
            )
        )

        row = cursor.fetchone()

        if not row:
            return

        total_files = row["total_files"]

        percentage = (
            int((processed_files / total_files) * 100)
            if total_files > 0
            else 0
        )

        cursor.execute(
            """
            UPDATE model_training_queue
            SET

                processed_files=%s,

                current_file=%s,

                progress_percentage=%s

            WHERE user_id=%s
            AND type=%s
            """,
            (
                processed_files,
                current_file,
                percentage,
                user_id,
                job_type
            )
        )

        conn.commit()

        cursor.close()
        conn.close()
        
    @staticmethod
    def mark_completed(
        user_id,
        job_type
    ):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE model_training_queue
            SET status='completed'
            WHERE user_id=%s
            AND type=%s
            AND status IN ('pending', 'uploading', 'training')
            """,
            (
                user_id,
                job_type
            )
        )

        conn.commit()

        cursor.close()
        conn.close()