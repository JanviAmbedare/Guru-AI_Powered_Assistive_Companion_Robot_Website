from services.whatsapp_service import (
    WhatsAppService
)
from config.settings import settings

result = WhatsAppService.send_message(

    settings.PHONE_NUMBER,

    "🚨 GURU TEST MESSAGE"

)

print(result)