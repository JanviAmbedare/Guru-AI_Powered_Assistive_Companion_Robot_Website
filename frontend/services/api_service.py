import requests


# =========================
# 🌐 BASE CONFIG
# =========================

import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "http://127.0.0.1:8000"
)

DEFAULT_TIMEOUT = 20


# =========================
# 🌐 COMMON API ENGINE
# =========================

def api_request(
    method,
    endpoint,
    token=None,
    data=None,
    files=None,
    params=None
):

    url = f"{API_BASE_URL}{endpoint}"

    headers = {}

    # =========================
    # 🔐 AUTH TOKEN
    # =========================

    if token:

        headers[
            "Authorization"
        ] = f"Bearer {token}"

    try:

        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data,
            files=files,
            params=params,
            timeout=DEFAULT_TIMEOUT
        )

        print("\n=========================")
        print(f"🌐 {method} {url}")
        print("📡 STATUS:",
              response.status_code)

        # =========================
        # ✅ JSON RESPONSE
        # =========================

        if response.headers.get(
            "content-type",
            ""
        ).startswith(
            "application/json"
        ):

            return response.json()

        # =========================
        # ❌ RAW RESPONSE
        # =========================

        return {
            "status": "error",
            "message": response.text
        }

    except requests.exceptions.ConnectionError:

        return {
            "status": "error",
            "message":
                "Backend server not running"
        }

    except requests.exceptions.Timeout:

        return {
            "status": "error",
            "message":
                "Request timeout"
        }

    except Exception as e:

        return {
            "status": "error",
            "message": str(e)
        }


# =====================================================
# 🔐 AUTH APIs
# =====================================================

def signup_user(data):

    return api_request(
        "POST",
        "/auth/register",
        data=data
    )


def login_user(data):

    return api_request(
        "POST",
        "/auth/login",
        data=data
    )


# =====================================================
# 👤 USER APIs
# =====================================================

def get_users(token):

    return api_request(
        "GET",
        "/dashboard/users",
        token=token
    )


def get_profile(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/profile/{user_id}",
        token=token
    )


# =====================================================
# 💬 CHAT APIs
# =====================================================

def send_chat(
    data,
    token
):

    return api_request(
        "POST",
        "/chat/",
        token=token,
        data=data
    )


def get_chat(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/memory/conversation/{user_id}",
        token=token
    )


# =====================================================
# 🧠 MEMORY APIs
# =====================================================

def get_conversation(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/memory/conversation/{user_id}",
        token=token
    )


def search_memory(
    user_id,
    query,
    token
):

    return api_request(
        "GET",
        f"/memory/search/{user_id}",
        token=token,
        params={
            "query": query
        }
    )


def get_memory_summary(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/memory/summary/{user_id}",
        token=token
    )


# =====================================================
# ⏰ REMINDER APIs
# =====================================================

def get_reminders(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/reminder/{user_id}",
        token=token
    )


def get_today_reminders(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/reminder/today/{user_id}",
        token=token
    )


def create_reminder(
    data,
    token
):

    return api_request(
        "POST",
        "/reminder/",
        token=token,
        data=data
    )


def mark_reminder_done(
    user_id,
    reminder_id,
    token
):

    return api_request(
        "PUT",
        f"/reminder/done/{user_id}/{reminder_id}",
        token=token
    )


def snooze_reminder(
    user_id,
    reminder_id,
    snooze_time,
    token
):

    return api_request(
        "PUT",
        f"/reminder/snooze/{user_id}/{reminder_id}",
        token=token,
        params={
            "snooze_time":
                snooze_time
        }
    )


def delete_reminder(
    user_id,
    reminder_id,
    token
):

    return api_request(
        "DELETE",
        f"/reminder/{user_id}/{reminder_id}",
        token=token
    )


# =====================================================
# 🚨 ALERT APIs
# =====================================================

def get_alerts(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/alerts/{user_id}",
        token=token
    )
#  =====================================================
# 📁 MEDIA APIs
# =====================================================
def get_media_status(
    user_id,
    token
):

    return api_request(
        "GET",
        f"{API_BASE_URL}/media/status/{user_id}",
        token=token
    )
def send_emergency_alert(
    user_id,
    message,
    token
):

    return api_request(
        "POST",
        f"{API_BASE_URL}/alerts/emergency",
        token=token,
        params={
            "user_id": user_id,
            "message": message
        }
    )


def critical_alert(
    user_id,
    message,
    token
):

    return api_request(
        "POST",
        f"{API_BASE_URL}/alerts/critical",
        token=token,
        params={
            "user_id": user_id,
            "message": message
        }
    )


def info_alert(
    user_id,
    message,
    token
):

    return api_request(
        "POST",
        f"{API_BASE_URL}/alerts/info",
        token=token,
        params={
            "user_id": user_id,
            "message": message
        }
    )


def acknowledge_alert(
    alert_id,
    token
):

    return api_request(
        "PUT",
        f"{API_BASE_URL}/alerts/acknowledge/{alert_id}",
        token=token
    )


def resolve_alert(
    alert_id,
    token
):

    return api_request(
        "PUT",
        f"{API_BASE_URL}/alerts/resolve/{alert_id}",
        token=token
    )


def alert_analytics(
    user_id,
    token
):

    return api_request(
        "GET",
        f"{API_BASE_URL}/alerts/analytics/{user_id}",
        token=token
    )
# =====================================================
# 🤖 ROBOT APIs
# =====================================================

def get_robot_status(
    robot_id,
    token
):

    return api_request(
        "GET",
        f"{API_BASE_URL}/robot/status/{robot_id}",
        token=token
    )


def send_robot_command(
    robot_id,
    data,
    token
):

    return api_request(
        "POST",
        f"{API_BASE_URL}/robot/command/{robot_id}",
        token=token,
        data=data
    )


# =====================================================
# 📸 FACE APIs
# =====================================================

def upload_face_samples(
    user_id,
    files,
    media_role,
    token
):

    return api_request(

        "POST",

        f"{API_BASE_URL}/media/register/face/{user_id}",

        token=token,

        files=files,

        data={
            "media_role":
                media_role
        }
    )
# =====================================================
# 🎤 VOICE APIs
# =====================================================

def upload_voice_samples(
    user_id,
    files,
    media_role,
    token
):

    return api_request(

        "POST",

        f"{API_BASE_URL}/media/register/voice/{user_id}",

        token=token,

        files=files,

        data={
            "media_role":
                media_role
        }
    )

# =====================================================
#  CLEAR USER MEDIA
# =====================================================
def clear_user_media(user_id):

    return requests.delete(
        f"{API_BASE_URL}/media/user/{user_id}"
    )

# =====================================================
# 🧠 TRAINING STATUS
# =====================================================
def get_training_status(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/training/status/{user_id}",
        token=token
    )

# =====================================================
# 🧠 AI TRAINING APIs
# =====================================================
def train_face_model(
    user_id,
    token
):

    return api_request(

        "POST",

        f"/training/face/{user_id}",

        token=token
    )

# =====================================================
# 🎤 VOICE MODEL TRAINING
# =====================================================
def train_voice_model(
    user_id,
    token
):

    return api_request(

        "POST",

        f"/training/voice/{user_id}",

        token=token
    )

# =====================================================
# 📊 ANALYTICS APIs
# =====================================================

def get_usage_stats(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/analytics/{user_id}",
        token=token
    )


def get_logs(
    user_id,
    token
):

    return api_request(
        "GET",
        f"/logs/{user_id}",
        token=token
    )


# =====================================================
# ❤️ HEALTH CHECK
# =====================================================

def health_check():

    return api_request(
        "GET",
        "/health"
    )