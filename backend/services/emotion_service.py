from database.db_connection import get_connection


class EmotionService:

    @staticmethod
    def get_latest(user_id: int):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                emotion,
                confidence,
                source_text,
                created_at
            FROM emotion_logs
            WHERE user_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """, (user_id,))

        emotion = cursor.fetchone()

        cursor.close()
        conn.close()

        return emotion or {
            "emotion": "unknown",
            "confidence": 0,
            "source_text": None,
            "created_at": None
        }
    @staticmethod
    def get_history(
        user_id: int,
        limit: int = 50
    ):

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                emotion,
                confidence,
                source_text,
                created_at
            FROM emotion_logs
            WHERE user_id=%s
            ORDER BY created_at DESC
            LIMIT %s
        """, (user_id, limit))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows