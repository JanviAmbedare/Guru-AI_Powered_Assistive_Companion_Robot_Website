from backend.services.whatsapp_service import (
    WhatsAppService
)
from backend.config.settings import settings

result = WhatsAppService.send_message(

    settings.PHONE_NUMBER,

    "🚨 GURU TEST MESSAGE"

)

print(result)