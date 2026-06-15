from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    make_response,
    jsonify
)

from functools import wraps
import traceback
import os
import base64
from datetime import datetime
from flask_cors import CORS
from services.api_service import *

from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)
CORS(
    app,
    supports_credentials=True
)
# =========================
# 📦 FILE LIMITS
# =========================

app.config[
    "MAX_CONTENT_LENGTH"
] = 50 * 1024 * 1024

# =========================
# 🔐 CONFIG
# =========================

app.secret_key = os.getenv("SECRET_KEY")

SESSION_TIMEOUT = 60 * 60 * 24
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

# =========================
# 🌐 GLOBAL TEMPLATE VARS
# =========================

@app.context_processor
def inject_globals():

    return {

        "API_BASE_URL":
        os.getenv(
            "API_BASE_URL",

            "https://guru-ai-powered-assistive-companion-kpna.onrender.com"
        )
    }

# =========================
# 🛡️ SAFE API WRAPPER
# =========================

def safe_api_call(func, *args, **kwargs):

    try:

        response = func(*args, **kwargs)

        if isinstance(response, dict):

            if response.get("status") == "error":
                print("API ERROR:", response)

        return response

    except Exception as e:

        print("SAFE API ERROR:", e)
        traceback.print_exc()

        return {
            "status": "error",
            "message": str(e)
        }


# =========================
# 🔐 LOGIN REQUIRED
# =========================

def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        if "token" not in session:
            return redirect("/login")

        return f(*args, **kwargs)

    return decorated


# =========================
# 🔐 ROLE REQUIRED
# =========================

def role_required(role):

    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):

            if session.get("role") != role:
                return "Unauthorized", 403

            return f(*args, **kwargs)

        return decorated

    return decorator


# =========================
# 🔐 AUTO LOGIN
# =========================

@app.before_request
def auto_login():

    if "token" not in session:

        token = request.cookies.get("token")

        if token:
            session["token"] = token


# =========================
# ❤️ HEALTH CHECK
# =========================

@app.route("/health")
def health():

    backend = safe_api_call(
        health_check
    )

    return jsonify({
        "frontend": "healthy",
        "backend": backend
    })


# =========================
# 🔐 LOGIN
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        data = {
            "name": request.form["name"],
            "password": request.form["password"]
        }

        response = safe_api_call(
            login_user,
            data
        )

        if "access_token" in response:

            session["token"] = response["access_token"]
            session["user_id"] = response["user_id"]
            session["role"] = response["role"]
            session["username"] = data["name"]
            
            resp = make_response(
                redirect("/")
            )

            # remember me
            if "remember" in request.form:

                resp.set_cookie(
                    "token",
                    response["access_token"],
                    max_age=SESSION_TIMEOUT
                )

            return resp

        return render_template(
            "login.html",
            error="Invalid credentials"
        )

    return render_template("login.html")


# =========================
# 📝 SIGNUP
# =========================

@app.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        data = {
            "name": request.form["name"],
            "password": request.form["password"],
            "role": request.form["role"]
        }

        result = safe_api_call(
            signup_user,
            data
        )

        user_id = result.get("user_id")

        if not user_id:

            return render_template(
                "signup.html",
                error=result.get(
                    "message",
                    "Signup failed"
                )
            )

        # AUTO LOGIN
        login_result = safe_api_call(
            login_user,
            {
                "name": data["name"],
                "password": data["password"]
            }
        )

        if "access_token" not in login_result:

            return "Auto login failed"

        session["token"] = (
            login_result["access_token"]
        )

        session["user_id"] = (
            login_result["user_id"]
        )

        session["role"] = (
            login_result["role"]
        )
        session["username"] = data["name"]
        return redirect(
            f"/capture-face/{user_id}"
        )

    return render_template("signup.html")


# =========================
# 📸 FACE PAGE
# =========================

@app.route("/capture-face/<int:user_id>")
@login_required
def capture_face(user_id):

    return render_template(
        "capture_face.html",
        user_id=user_id
    )


# =========================
# 📸 FACE REGISTER API
# =========================

# @app.route(
#     "/register/face/<int:user_id>",
#     methods=["POST"]
# )
# @login_required
# def register_face(user_id):

#     try:

#         files = request.files.getlist("files")

#         media_role = request.form.get(
#             "media_role",
#             "raw"
#         )

#         result = upload_face_samples(

#             user_id=user_id,

#             files=[
#                 (
#                     "files",
#                     (
#                         file.filename,
#                         file.stream,
#                         file.mimetype
#                     )
#                 )
#                 for file in files
#             ],

#             media_role=media_role,

#             token=session["token"]
#         )

#         return jsonify(result)

#     except Exception as e:

#         print(
#             "FACE REGISTER ERROR:",
#             str(e)
#         )

#         traceback.print_exc()

#         return jsonify({

#             "status": "error",

#             "message": str(e)

#         }), 500
# =========================
# 🎤 VOICE PAGE
# =========================

@app.route("/capture-voice/<int:user_id>")
@login_required
def capture_voice(user_id):

    return render_template(
        "capture_voice.html",
        user_id=user_id
    )

# =========================
# 🎤 VOICE REGISTER API
# =========================

# @app.route(
#     "/register/voice/<int:user_id>",
#     methods=["POST"]
# )
# @login_required
# def register_voice(user_id):

#     try:

#         files = request.files.getlist("files")

#         media_role = request.form.get(
#             "media_role",
#             "raw"
#         )

#         result = upload_voice_samples(

#             user_id=user_id,

#             files=[
#                 (
#                     "files",
#                     (
#                         file.filename,
#                         file.stream,
#                         file.mimetype
#                     )
#                 )
#                 for file in files
#             ],

#             media_role=media_role,

#             token=session["token"]
#         )

#         return jsonify(result)

#     except Exception as e:

#         print(
#             "VOICE REGISTER ERROR:",
#             str(e)
#         )

#         traceback.print_exc()

#         return jsonify({

#             "status": "error",

#             "message": str(e)

#         }), 500

# =========================
# ✅ REGISTRATION COMPLETE
# =========================
@app.route(
    "/registration-complete/<int:user_id>"
)
@login_required
def registration_complete(
    user_id
):

    return render_template(
        "registration_full.html",
        user_id=user_id
    )

# =========================
# 🗝️ AUTO LOGIN (FACE/VOICE)
# =========================
@app.route(
    "/upload-media/<int:user_id>",
    methods=["POST"]
)
@login_required
def upload_media(user_id):

    try:

        face_files = request.files.getlist(
            "face_files"
        )

        voice_files = request.files.getlist(
            "voice_files"
        )

        result = upload_all_media(
            user_id=user_id,
            face_files=face_files,
            voice_files=voice_files,
            token=session["token"]
        )

        return jsonify(result)

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500

# =========================
# 🚪 TRAIN FACE MODEL
# =========================
@app.route(
    "/train-face/<int:user_id>",
    methods=["POST"]
)
@login_required
def train_face_route(
    user_id
):

    result = train_face_model(
        user_id,
        session["token"]
    )

    return jsonify(result)

# =========================
# 🚪 TRAIN VOICE MODEL
# =========================
@app.route(
    "/train-voice/<int:user_id>",
    methods=["POST"]
)
@login_required
def train_voice_route(
    user_id
):

    result = train_voice_model(
        user_id,
        session["token"]
    )

    return jsonify(result)

# =========================
# 🏠 DASHBOARD
# =========================

@app.route("/")
@login_required
def dashboard():

    return render_template(
        "dashboard.html",
        role=session["role"],
        user_id=session["user_id"]
    )


# =========================
# 💬 CHAT
# =========================

@app.route("/chat")
@login_required
def chat():

    conversations = safe_api_call(
        get_chat,
        session["user_id"],
        session["token"]
    )

    return render_template(
        "chat_modern.html",
        conversations=conversations
    )

# =========================
# 🧠 MEMORY
# =========================

@app.route("/memory/<int:user_id>", methods=["GET"])
@login_required
def memory(user_id):

    conversations = safe_api_call(
        get_conversation,
        user_id,
        session["token"]
    )

    return render_template(
        "memory.html",
        conversations=conversations
    )


# =========================
# 🤖 ROBOT
# =========================

@app.route("/robot", methods=["GET"])
@login_required
@role_required("OWNER")
def robot():

    status = safe_api_call(
        get_robot_status,
        session["token"]
    )

    return render_template(
        "robot.html",
        status=status
    )


# =========================
# 🚨 ALERTS PAGE
# =========================

@app.route(
    "/alerts/<int:user_id>"
)
@login_required
def alerts(user_id):

    alerts_data = safe_api_call(
        get_alerts,
        user_id,
        session["token"]
    )

    analytics = safe_api_call(
        alert_analytics,
        user_id,
        session["token"]
    )

    return render_template(
        "alerts.html",
        alerts=alerts_data,
        analytics=analytics,
        user_id=user_id
    )


# =========================
# 🚨 EMERGENCY ALERT
# =========================

@app.route(
    "/trigger-emergency",
    methods=["POST"]
)
@login_required
def trigger_emergency():

    data = request.json

    result = safe_api_call(
        send_emergency_alert,
        session["user_id"],
        data["message"],
        session["token"]
    )

    return jsonify(result)


# =========================
# ✅ ACKNOWLEDGE ALERT
# =========================

@app.route(
    "/ack-alert/<int:alert_id>",
    methods=["PUT"]
)
@login_required
def ack_alert(alert_id):

    result = safe_api_call(
        acknowledge_alert,
        alert_id,
        session["token"]
    )

    return jsonify(result)

# =========================
# 🔴 LIVE ALERTS API
# =========================

@app.route(
    "/api/live-alerts/<int:user_id>"
)
@login_required
def live_alerts(user_id):

    alerts_data = safe_api_call(
        get_alerts,
        user_id,
        session["token"]
    )

    active_alerts = []

    for alert in alerts_data:

        if alert["status"] == "ACTIVE":

            active_alerts.append(alert)

    return jsonify(active_alerts)

# =========================
# ⏰ REMINDERS
# =========================

@app.route(
    "/reminders/<int:user_id>",
    methods=["GET"]
)
@login_required
def reminders(user_id):

    reminders_data = safe_api_call(
        get_reminders,
        user_id,
        session["token"]
    )

    return render_template(
        "reminders.html",
        reminders=reminders_data,
        user_id=user_id
    )



# =========================
# 📊 LOGS
# =========================

@app.route("/logs/<int:user_id>", methods=["GET"])
@login_required
def logs(user_id):

    logs_data = safe_api_call(
        get_logs,
        user_id,
        session["token"]
    )

    return render_template(
        "logs.html",
        logs=logs_data
    )


# =========================
# 🚪 LOGOUT
# =========================

@app.route("/logout")
def logout():

    session.clear()

    resp = make_response(
        redirect("/login")
    )

    resp.delete_cookie("token")

    return resp


# =========================
# ❌ ERROR HANDLERS
# =========================

@app.errorhandler(404)
def not_found(e):

    return render_template(
        "404.html"
    ), 404


@app.errorhandler(500)
def server_error(e):

    return render_template(
        "500.html"
    ), 500


# =========================
# 🚀 RUN
# =========================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )