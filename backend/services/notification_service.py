import threading

from services.whatsapp_service import (
    WhatsAppService
)


from services.logging_service import (
    LoggingService
)


class NotificationService:

    @staticmethod
    def send_all(
        whatsapp_to,
        title,
        message
    ):

        results = {}

        # =========================
        # 💬 WHATSAPP
        # =========================

        try:

            threading.Thread(

                target=WhatsAppService.send_message,

                args=(
                    whatsapp_to,
                    message
                ),

                daemon=True

            ).start()

            results["whatsapp"] = "started"

        except Exception as e:

            results["whatsapp"] = str(e)

        # =========================
        # 🔔 PUSH
        # =========================

        #alert.js will handle push notifications on the frontend, so we just log it here

        LoggingService.info(
            f"Notification sent: "
            f"{title}"
        )

        return results