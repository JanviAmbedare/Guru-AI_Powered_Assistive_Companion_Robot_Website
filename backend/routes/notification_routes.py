from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.notification_service import (
    NotificationService
)

router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


class NotificationRequest(BaseModel):
    whatsapp_to: str
    subscription: dict
    message: str


@router.post("/send")
def send_notification(data: NotificationRequest):

    return NotificationService.send_all(
        data.whatsapp_to,
        data.subscription,
        data.message
    )