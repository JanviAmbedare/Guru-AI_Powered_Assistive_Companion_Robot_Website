from database.db_connection import get_connection

class ConversationService:
    @staticmethod
    def get_history(
        user_id: int,
        limit: int = 20
    ):

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                user_input,
                response_text,
                intent,
                emotion,
                timestamp
            FROM voice_interactions
            WHERE user_id=%s
            ORDER BY timestamp DESC
            LIMIT %s
        """, (user_id, limit))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows


    @staticmethod
    def get_analytics(
        user_id: int
    ):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                intent,
                COUNT(*) as count
            FROM voice_interactions
            WHERE user_id=%s
            GROUP BY intent
            ORDER BY count DESC
        """, (user_id,))

        intents = cursor.fetchall()

        cursor.execute("""
            SELECT
                emotion,
                COUNT(*) as count
            FROM emotion_logs
            WHERE user_id=%s
            GROUP BY emotion
        """, (user_id,))

        emotions = cursor.fetchall()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM voice_interactions
            WHERE user_id=%s
        """, (user_id,))

        total = cursor.fetchone()

        cursor.close()
        conn.close()

        return {
            "total_interactions":
                total["total"],

            "top_intents":
                intents,

            "emotion_distribution":
                emotions
        }