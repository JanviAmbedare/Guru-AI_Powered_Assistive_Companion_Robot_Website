# import joblib
# from datetime import datetime

# from database.memory_manager import MemoryManager
# from database.profile_manager import UserProfileManager
# from database.reminder_manager import ReminderManager
# from config.settings import Settings
# from services.robot_service import RobotService
# from services.alert_service import AlertService
# from services.logging_service import LoggingService
# # from services.context_memory_service import (
# #     ContextMemoryService
# # )

# HF_TOKEN = Settings.HF_TOKEN

# # =========================
# # 🧠 LOAD INTENT MODEL
# # =========================

# intent_pipeline = joblib.load(
#     "backend/models/intent_pipeline.pkl"
# )


# # =========================
# # 🤖 GURU AI ENGINE
# # =========================

# class GuruAIService:

#     # =========================
#     # 🎯 INTENT DETECTION
#     # =========================

#     @staticmethod
#     def detect_intent(text: str):

#         try:
#             prediction = intent_pipeline.predict([text])[0]
#             return prediction

#         except Exception as e:

#             LoggingService.error(
#                 f"Intent Detection Error: {e}"
#             )

#             return "fallback"

#     # =========================
#     # 😊 SENTIMENT ANALYSIS
#     # =========================

#     @staticmethod
#     def detect_sentiment(text: str):

#         text = text.lower()

#         positive_words = [
#             "happy",
#             "good",
#             "great",
#             "awesome",
#             "excellent"
#         ]

#         negative_words = [
#             "sad",
#             "bad",
#             "angry",
#             "depressed",
#             "stress"
#         ]

#         if any(w in text for w in positive_words):
#             return "positive"

#         if any(w in text for w in negative_words):
#             return "negative"

#         return "neutral"

#     # =========================
#     # 🧠 LOAD MEMORY
#     # =========================

#     @staticmethod
#     def load_memory(user_id):

#         mm = MemoryManager(user_id)

#         try:
#             return mm.get_recent_context(limit=5)

#         except:
#             return []

#     # =========================
#     # ⚡ ACTION ENGINE
#     # =========================

#     @staticmethod
#     def execute_action(
#         user_id,
#         intent,
#         text
#     ):

#         # ⏰ REMINDER
#         if intent == "reminder":

#             rm = ReminderManager(user_id)

#             remind_time = datetime.now()

#             rm.add_reminder(
#                 text,
#                 remind_time,
#                 "NONE"
#             )

#             return "Reminder created successfully."

#         # 🚨 EMERGENCY
#         elif intent == "emergency":

#             AlertService.emergency_alert(
#                 user_id,
#                 text
#             )

#             return "Emergency alert triggered."

#         # 🤖 ROBOT MOVE
#         elif intent == "robot_move":

#             RobotService.move_forward()

#             return "Robot moving forward."

#         # 🛑 ROBOT STOP
#         elif intent == "robot_stop":

#             RobotService.stop()

#             return "Robot stopped."

#         return None

#     # =========================
#     # 💬 RESPONSE GENERATION
#     # =========================

#     @staticmethod
#     def generate_contextual_response(
#         user_id,
#         text,
#         intent,
#         emotion
#     ):

#         # memories = (
#         #     ContextMemoryService
#         #     .search_similar_memories(
#         #         user_id,
#         #         text
#         #     )
#         # )

#         memory_context = ""

#         for m in memories:

#             memory_context += (
#                 f"- {m['memory']['summary']}\n"
#             )

#         prompt = f"""
#         You are GURU AI.

#         User emotion:
#         {emotion}

#         Relevant memories:
#         {memory_context}

#         User message:
#         {text}

#         Reply naturally,
#         emotionally,
#         and contextually.
#         """

#         # future LLM integration here

#         return (
#             f"I understand your request. "
#             f"Based on our previous interactions, "
#             f"I'll help you with this."
#         )

#     # =========================
#     # 🧠 MAIN AI PIPELINE
#     # =========================

#     @staticmethod
#     def process_message(
#         user_id,
#         text
#     ):

#         # 🎯 DETECT INTENT
#         intent = GuruAIService.detect_intent(text)

#         # 😊 SENTIMENT
#         sentiment = GuruAIService.detect_sentiment(text)

#         # ⚡ EXECUTE ACTION
#         action_response = GuruAIService.execute_action(
#             user_id,
#             intent,
#             text
#         )

#         # 💬 AI RESPONSE
#         if action_response:

#             response = action_response

#         else:

#             response = GuruAIService.generate_contextual_response(
#                 user_id,
#                 intent,
#                 text,
#                 sentiment
#             )

#         # 🧠 SAVE MEMORY
#         try:

#             mm = MemoryManager(user_id)

#             mm.save_conversation(
#                 text,
#                 intent,
#                 response,
#                 sentiment
#             )

#         except Exception as e:

#             LoggingService.error(
#                 f"Memory Save Error: {e}"
#             )

#         # 📊 LOGGING
#         LoggingService.info(
#             f"[AI CHAT] User={user_id} "
#             f"Intent={intent} "
#             f"Sentiment={sentiment}"
#         )

#         return {
#             "intent": intent,
#             "sentiment": sentiment,
#             "response": response
#         }