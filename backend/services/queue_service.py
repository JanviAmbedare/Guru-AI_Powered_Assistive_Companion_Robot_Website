class QueueService:

    @staticmethod
    def add_job(
        user_id,
        job_type
    ):

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO model_training_queue
            (
                user_id,
                type,
                status
            )
            VALUES
            (%s,%s,'pending')
            """,
            (
                user_id,
                job_type
            )
        )

        conn.commit()

        cursor.close()
        conn.close()