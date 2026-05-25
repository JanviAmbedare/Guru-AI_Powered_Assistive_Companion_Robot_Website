from fastapi import APIRouter

from backend.services.alert_service import (
    AlertService
)

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)


# =========================
# 📥 GET ALERTS
# =========================

@router.get("/{user_id}")
def get_alerts(user_id: int):

    return AlertService.get_alerts(
        user_id
    )


# =========================
# 🚨 EMERGENCY
# =========================

@router.post("/emergency")
def emergency_alert(
    user_id: int,
    message: str
):

    return AlertService.emergency_alert(
        user_id,
        message
    )


# =========================
# ⚠️ CRITICAL
# =========================

@router.post("/critical")
def critical_alert(
    user_id: int,
    message: str
):

    return AlertService.critical_alert(
        user_id,
        message
    )


# =========================
# ℹ️ INFO
# =========================

@router.post("/info")
def info_alert(
    user_id: int,
    message: str
):

    return AlertService.info_alert(
        user_id,
        message
    )


# =========================
# ✅ ACKNOWLEDGE
# =========================

@router.put("/acknowledge/{alert_id}")
def acknowledge_alert(
    alert_id: int
):

    return AlertService.acknowledge_alert(
        alert_id
    )


# =========================
# ✔️ RESOLVE
# =========================

@router.put("/resolve/{alert_id}")
def resolve_alert(
    alert_id: int
):

    return AlertService.resolve_alert(
        alert_id
    )


# =========================
# 📊 ANALYTICS
# =========================

@router.get("/analytics/{user_id}")
def analytics(user_id: int):

    return AlertService.alert_analytics(
        user_id
    )