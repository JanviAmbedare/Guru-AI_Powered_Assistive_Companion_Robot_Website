from backend.database.db_utils import execute_query
from collections import Counter

class DailySummaryService:

    @staticmethod
    def generate_summary(user_id):

        conversations = execute_query("""
            SELECT *
            FROM conversations
            WHERE user_id=%s
            AND DATE(timestamp)=CURDATE()
        """,(user_id,),
        fetch=True,
        dictionary=True)

        if not conversations:
            return {
                "summary":"No activity today"
            }

        intents = [
            c["intent"]
            for c in conversations
        ]

        sentiments = [
            c["sentiment"]
            for c in conversations
        ]

        top_intent = Counter(intents).most_common(1)[0][0]
        top_emotion = Counter(sentiments).most_common(1)[0][0]

        important = conversations[-3:]

        return {
            "total_conversations":len(conversations),
            "top_intent":top_intent,
            "top_emotion":top_emotion,
            "important_memories":important,
            "summary":
            f"""
            User interacted {len(conversations)} times today.
            Dominant emotion was {top_emotion}.
            Most common activity was {top_intent}.
            """
        }