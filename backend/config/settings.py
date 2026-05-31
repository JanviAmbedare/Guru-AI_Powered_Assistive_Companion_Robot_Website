import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # =========================
    # APP CONFIG
    # =========================
    APP_NAME = "GURU Backend"
    VERSION = "2.0"
    DEBUG = os.getenv("DEBUG", "True") == "True"

    # =========================
    # SERVER CONFIG
    # =========================
    HOST = os.getenv("HOST", "127.0.0.1")
    PORT = int(os.getenv("PORT", 8000))

    # =========================
    # DATABASE CONFIG
    # =========================
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT"))
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")

    # =========================
    # STORAGE CONFIG
    # =========================
    BASE_STORAGE_PATH = os.getenv("BASE_STORAGE_PATH", "../storage")

    FACE_STORAGE = os.path.join(BASE_STORAGE_PATH, "faces")
    VOICE_STORAGE = os.path.join(BASE_STORAGE_PATH, "voices")

    # =========================
    # SECURITY CONFIG
    # =========================
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 60
    # =========================
    # TWILIO CONFIG
    # =========================
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    PHONE_NUMBER = os.getenv("ALERT_PHONE")  # Your Twilio phone number SMS
    TWILIO_FROM_NUMBER = os.getenv("TWILIO_PHONE")  # Your Twilio phone number for sending messages
    FROM_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_FROM")     # Your Twilio phone number for WhatsApp
    TO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_TO")   # Your phone number for receiving WhatsApp messages
    # =========================
    # API CONFIG (Frontend ↔ Backend)
    # =========================
    BASE_API_URL = os.getenv("BASE_API_URL", "http://127.0.0.1:8000")
    # =========================
    # HUGGING FACE (AI) CONFIG
    # =========================
    HF_TOKEN = os.getenv("HF_TOKEN")
    # =========================
    # AI SERVICE CONFIG (Backend ↔ AI Service)
    # =========================
    AI_SERVICE_URL = os.getenv(
    "AI_SERVICE_URL",
    "http://localhost:8001"
)
    # =========================
    # AI MODEL CONFIG
    # =========================
    MODEL_PATH = os.getenv("MODEL_PATH", "models/")
    FACE_MODEL_PATH = os.path.join(MODEL_PATH, "face_model")
    VOICE_MODEL_PATH = os.path.join(MODEL_PATH, "voice_model")

    # =========================
    # LOGGING CONFIG
    # =========================
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()