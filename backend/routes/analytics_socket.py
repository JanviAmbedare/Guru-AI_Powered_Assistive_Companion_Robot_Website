from fastapi import APIRouter
from fastapi import WebSocket
from fastapi import WebSocketDisconnect

import asyncio


router = APIRouter()

@router.websocket(
    "/ws/analytics/{user_id}"
)
async def analytics_socket(
    websocket: WebSocket,
    user_id: int
):

    await websocket.accept()

    print(
        f"Analytics connected: {user_id}"
    )

    try:

        while True:

            data = {

                "conversations":{
                    "total": None

                },

                "robot":{

                    "battery_level":
                        None,

                    "cpu_temp":
                        None
                },

                "emotions":[

                    {
                        "emotion":"happy",
                        "total":None
                    },

                    {
                        "emotion":"stress",
                        "total":None
                    }
                ],

                "intents":[

                    {
                        "intent":"reminder",
                        "total":None
                    },

                    {
                        "intent":"health",
                        "total":None
                    }
                ]
            }

            await websocket.send_json(data)

            await asyncio.sleep(2)

    except WebSocketDisconnect:

        print(
            f"Disconnected: {user_id}"
        )