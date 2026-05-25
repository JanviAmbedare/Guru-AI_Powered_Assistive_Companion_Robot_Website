from twilio.rest import Client

from backend.config.settings import settings

from backend.services.logging_service import (
    LoggingService
)


ACCOUNT_SID = settings.TWILIO_ACCOUNT_SID

AUTH_TOKEN = settings.TWILIO_AUTH_TOKEN

FROM_NUMBER = settings.FROM_WHATSAPP_NUMBER



class WhatsAppService:

    @staticmethod
    def send_message(
        to_number,
        message
    ):

        try:

            print(
                "📤 Sending WhatsApp..."
            )

            client = Client(
                ACCOUNT_SID,
                AUTH_TOKEN
            )

            msg = client.messages.create(

                body=message,

                from_=FROM_NUMBER,

                to=f"whatsapp:{to_number}"
            )

            print(
                "✅ WhatsApp Sent:",
                msg.sid
            )

            LoggingService.info(
                f"WhatsApp sent to "
                f"{to_number}"
            )

            return {
                "status": "success",
                "sid": msg.sid
            }

        except Exception as e:

            print(
                "❌ WhatsApp Error:",
                str(e)
            )

            LoggingService.error(
                f"WhatsApp Error: {e}"
            )

            return {
                "status": "error",
                "message": str(e)
            }