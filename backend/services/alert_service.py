from datetime import datetime

from services.notification_service import NotificationService
from database.db_utils import execute_query
from services.whatsapp_service import WhatsAppService
from services.logging_service import (LoggingService)
from config.settings import settings
from services.robot_service import (    RobotService)

import threading

threading.Thread(

    target=WhatsAppService.send_message,

    args=(
        settings.PHONE_NUMBER,
        "Alert System Initialized. You will receive notifications here."
    ),

    daemon=True

).start()


class AlertService:

    # =========================
    # 🚨 CREATE ALERT
    # =========================

    @staticmethod
    def create_alert(
        user_id,
        title,
        message,
        alert_type="INFO",
        severity="LOW",
        source="SYSTEM"
    ):

        query = """
            INSERT INTO alerts
            (
                user_id,
                title,
                message,
                type,
                severity,
                source,
                status,
                created_at
            )
            VALUES
            (
                %s,%s,%s,%s,%s,%s,
                'ACTIVE',
                %s
            )
        """

        execute_query(
            query,
            (
                user_id,
                title,
                message,
                alert_type,
                severity,
                source,
                datetime.now()
            )
        )

        LoggingService.info(
            f"[ALERT CREATED] "
            f"User={user_id} "
            f"Type={alert_type}"
        )

        return {
            "status": "success",
            "message": "Alert created"
        }

    # =========================
    # 📥 GET ALERTS
    # =========================

    @staticmethod
    def get_alerts(
        user_id,
        limit=50
    ):

        query = """
            SELECT *
            FROM alerts
            WHERE user_id=%s
            ORDER BY created_at DESC
            LIMIT %s
        """

        return execute_query(
            query,
            (user_id, limit),
            fetch=True,
            dictionary=True
        )

    # =========================
    # 🚨 EMERGENCY ALERT
    # =========================

    @staticmethod
    def emergency_alert(
        user_id,
        message
    ):

        AlertService.create_alert(
            user_id=user_id,
            title="Emergency Alert",
            message=message,
            alert_type="EMERGENCY",
            severity="CRITICAL",
            source="AI_SYSTEM"
        )
        user = execute_query(
        """
        SELECT phone_number
        FROM users
        WHERE id=%s
        """,
        (user_id,),
        fetch_one=True,
        dictionary=True
        )

        phone = None

        if user:
            phone = user.get("phone_number")

        NotificationService.send_all(
            whatsapp_to=phone,
            title="GURU Emergency Alert",
            message=message
        )
        try:

            RobotService.speak(
                "Emergency detected. "
                "Sending emergency notification. "
                "Please stay calm. "
                "Help has been informed."
            )

        except Exception as e:

            print(e)

        LoggingService.warning(
            f"[EMERGENCY] {message}"
        )

        return {
            "status": "success",
            "message":
                "Emergency alert triggered"
        }

    # =========================
    # ⚠️ CRITICAL ALERT
    # =========================

    @staticmethod
    def critical_alert(
        user_id,
        message
    ):

        return AlertService.create_alert(
            user_id=user_id,
            title="Critical Alert",
            message=message,
            alert_type="CRITICAL",
            severity="HIGH",
            source="ROBOT_SYSTEM"
        )

    # =========================
    # ℹ️ INFO ALERT
    # =========================

    @staticmethod
    def info_alert(
        user_id,
        message
    ):

        return AlertService.create_alert(
            user_id=user_id,
            title="Info Alert",
            message=message,
            alert_type="INFO",
            severity="LOW",
            source="SYSTEM"
        )

    # =========================
    # ✅ ACKNOWLEDGE
    # =========================

    @staticmethod
    def acknowledge_alert(
        alert_id
    ):

        query = """
            UPDATE alerts
            SET
                status='ACKNOWLEDGED',
                acknowledged_at=NOW()
            WHERE id=%s
        """

        execute_query(
            query,
            (alert_id,)
        )

        return {
            "status": "success"
        }

    # =========================
    # ✔️ RESOLVE ALERT
    # =========================

    @staticmethod
    def resolve_alert(
        alert_id
    ):

        query = """
            UPDATE alerts
            SET
                status='RESOLVED',
                resolved_at=NOW()
            WHERE id=%s
        """

        execute_query(
            query,
            (alert_id,)
        )

        return {
            "status": "success"
        }

    # =========================
    # 📊 ALERT ANALYTICS
    # =========================

    @staticmethod
    def alert_analytics(
        user_id
    ):

        total = execute_query("""
            SELECT COUNT(*) as total
            FROM alerts
            WHERE user_id=%s
        """, (
            user_id,
        ), fetch_one=True, dictionary=True)

        critical = execute_query("""
            SELECT COUNT(*) as total
            FROM alerts
            WHERE user_id=%s
            AND severity='CRITICAL'
        """, (
            user_id,
        ), fetch_one=True, dictionary=True)

        active = execute_query("""
            SELECT COUNT(*) as total
            FROM alerts
            WHERE user_id=%s
            AND status='ACTIVE'
        """, (
            user_id,
        ), fetch_one=True, dictionary=True)

        return {
            "total_alerts":
                total["total"],

            "critical_alerts":
                critical["total"],

            "active_alerts":
                active["total"]
        }