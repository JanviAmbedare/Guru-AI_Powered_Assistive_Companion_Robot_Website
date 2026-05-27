import requests
from fastapi import APIRouter, WebSocket

router = APIRouter()

AI_SERVICE_URL = (
    "https://guru-ai-service.onrender.com/chat"
)

@router.websocket("/ws/chat/{user_id}")

async def websocket_chat(
    websocket: WebSocket,
    user_id: int
):

    await websocket.accept()

    while True:

        text = await websocket.receive_text()

        response = requests.post(
            AI_SERVICE_URL,
            json={
                "user_id": user_id,
                "message": text
            }
        )

        result = response.json()

        await websocket.send_json(result)