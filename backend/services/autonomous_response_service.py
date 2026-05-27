from services.emotion_service import EmotionPredictionService

class AutonomousResponseService:

    @staticmethod
    def generate(user_id):

        emotion = EmotionPredictionService.predict(user_id)

        if emotion["risk_level"] == "high":

            return {
                "action":"support",
                "message":
                """
                You seem emotionally stressed.
                Would you like calming music,
                breathing exercises,
                or emergency contact support?
                """
            }

        return {
            "action":"none"
        }