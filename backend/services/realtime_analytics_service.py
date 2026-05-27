from database.db_utils import execute_query

class RealtimeAnalyticsService:

    @staticmethod
    def get_dashboard_metrics(user_id):

        total_conversations = execute_query("""
            SELECT COUNT(*) as total
            FROM conversations_v2
            WHERE user_id=%s
        """, (
            user_id,
        ), fetch_one=True, dictionary=True)

        emotions = execute_query("""
            SELECT emotion, COUNT(*) as total
            FROM emotion_analytics
            WHERE user_id=%s
            GROUP BY emotion
        """, (
            user_id,
        ), fetch=True, dictionary=True)

        intents = execute_query("""
            SELECT intent, COUNT(*) as total
            FROM conversations_v2
            WHERE user_id=%s
            GROUP BY intent
        """, (
            user_id,
        ), fetch=True, dictionary=True)

        robot = execute_query("""
            SELECT *
            FROM robot_telemetry
            ORDER BY created_at DESC
            LIMIT 1
        """, fetch_one=True, dictionary=True)

        return {
            "conversations":
                total_conversations,

            "emotions":
                emotions,

            "intents":
                intents,

            "robot":
                robot
        }