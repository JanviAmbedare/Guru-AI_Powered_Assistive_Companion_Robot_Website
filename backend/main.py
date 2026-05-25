from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from backend.models.model_manager import ModelManager
from backend.routes import (
    registration_routes,
    dashboard_routes,
    reminder_routes,
    profile_routes,
    auth_routes,
    memory_routes,
    robot_routes,
    notification_routes,
    alert_routes,
    chat_routes,
    health_routes
)
from backend.routes.analytics_socket import (
    router as analytics_socket_router
)
from backend.routes.memory_routes import router as memory_router
import threading

from backend.services.reminder_scheduler import (
    ReminderScheduler
)

scheduler_thread = threading.Thread(
    target=ReminderScheduler.start,
    daemon=True
)

scheduler_thread.start()

from backend.services.logging_service import (
    LoggingService
)


# =========================
# 🚀 APP LIFECYCLE
# =========================

@asynccontextmanager
async def lifespan(app: FastAPI):

    LoggingService.info(
        "🚀 GURU Backend Started"
    )

    yield

    LoggingService.info(
        "🛑 GURU Backend Stopped"
    )


# =========================
# 🚀 FASTAPI APP
# =========================

app = FastAPI(
    title="GURU Backend API",
    version="3.0",
    description="""
    AI-Powered Assistive
    Companion Backend
    """,
    lifespan=lifespan
)


# =========================
# 🌍 CORS
# =========================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================
# 📡 ROUTERS
# =========================
# IMPORTANT:
# Route files already contain prefixes
# So DON'T duplicate prefixes here
# =========================

app.include_router(auth_routes.router)

app.include_router(registration_routes.router)

app.include_router(dashboard_routes.router)

app.include_router(reminder_routes.router)

app.include_router(profile_routes.router)

app.include_router(memory_routes.router)

app.include_router(chat_routes.router)

app.include_router(robot_routes.router)

app.include_router(alert_routes.router)

app.include_router(notification_routes.router)

app.include_router(health_routes.router)

app.include_router(
    analytics_socket_router
)

app.include_router(
    memory_router,
    prefix="/api/memory",
    tags=["Memory"]
)
# =========================
# 🏠 ROOT
# =========================

@app.get("/")
def home():

    return {
        "status": "GURU Backend Running",
        "version": "3.0",
        "ai": "active",
        "robotics": "enabled"
    }


# =========================
# ❤️ API HEALTH
# =========================

@app.get("/api")
def api_health():

    return {
        "status": "healthy",
        "message": "GURU API operational"
    }


# =========================
# ❌ GLOBAL ERROR HANDLER
# =========================

@app.exception_handler(Exception)
async def global_exception_handler(
    request,
    exc
):

    LoggingService.error(
        f"Unhandled Exception: {exc}"
    )

    return JSONResponse(
        status_code=500,
        content={
            "status": "error",
            "message": str(exc)
        }
    )
    

@app.on_event("startup")
async def startup_event():

    ModelManager.load_models()