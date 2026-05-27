# from transformers import pipeline
# from database.db_utils import execute_query
# from collections import Counter

# emotion_classifier = pipeline(
#     "text-classification",
#     model="j-hartmann/emotion-english-distilroberta-base"
# )

# class EmotionService:

#     @staticmethod
#     def detect(text):

#         result = emotion_classifier(text)[0]

#         return {
#             "emotion": result["label"],
#             "confidence": result["score"]
#         }

# class EmotionPredictionService:

#     @staticmethod
#     def predict(user_id):

#         emotions = execute_query("""
#             SELECT sentiment
#             FROM conversations
#             WHERE user_id=%s
#             ORDER BY timestamp DESC
#             LIMIT 20
#         """,(user_id,),
#         fetch=True,
#         dictionary=True)

#         if not emotions:
#             return {
#                 "prediction":"neutral"
#             }

#         vals = [
#             e["sentiment"]
#             for e in emotions
#         ]

#         dominant = Counter(vals).most_common(1)[0][0]

#         risk = "low"

#         negative = [
#             "sad",
#             "angry",
#             "fear",
#             "stress"
#         ]

#         negative_count = len([
#             v for v in vals
#             if v in negative
#         ])

#         if negative_count > 10:
#             risk = "high"

#         return {
#             "prediction":dominant,
#             "risk_level":risk
#         }