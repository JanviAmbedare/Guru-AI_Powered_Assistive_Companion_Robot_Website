from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)

from services.ai_client import AIClient

router = APIRouter()


@router.websocket(
    "/ws/chat/{user_id}"
)
async def websocket_chat(
    websocket: WebSocket,
    user_id: int
):

    await websocket.accept()

    try:

        while True:

            text = (
                await websocket.receive_text()
            )

            result = AIClient.chat(
                user_id=user_id,
                message=text
            )

            await websocket.send_json(
                result
            )

    except WebSocketDisconnect:

        print(
            f"User {user_id} disconnected"
        )

    except Exception as e:

        await websocket.send_json(
            {
                "status": "error",
                "message": str(e)
            }
        )