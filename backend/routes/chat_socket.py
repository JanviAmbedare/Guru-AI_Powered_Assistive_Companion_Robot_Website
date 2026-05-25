from fastapi import APIRouter, WebSocket
from backend.services.ai_service import GuruAIService

router = APIRouter()

@router.websocket("/ws/chat/{user_id}")
async def websocket_chat(
    websocket: WebSocket,
    user_id: int
):

    await websocket.accept()

    while True:

        text = await websocket.receive_text()

        response = (
            GuruAIService
            .process_message(
                user_id,
                text
            )
        )

        await websocket.send_json(response)