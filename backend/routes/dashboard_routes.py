from fastapi import APIRouter, HTTPException, Depends
from services.robot_service import RobotService
from database.db_connection import get_connection
from utils.dependencies import require_role, get_current_user
from database.db_utils import execute_query
from services.conversation_service import ConversationService
router = APIRouter()

# def execute_query(
#     query,
#     params=None,
#     fetch=False,
#     fetch_one=False,
#     dictionary=False
# ):
#     try:
#         conn = get_connection()

#         cursor = conn.cursor(
#             dictionary=dictionary
#         )

#         cursor.execute(
#             query,
#             params or ()
#         )

#         if fetch_one:
#             return cursor.fetchone()

#         if fetch:
#             return cursor.fetchall()

#         conn.commit()

#         return {
#             "status": "success"
#         }

#     except Exception as e:

#         raise HTTPException(
#             status_code=500,
#             detail=str(e)
#         )

#     finally:

#         cursor.close()
#         conn.close()


@router.get("/dashboard/users")
def get_users(user=Depends(require_role("OWNER"))):
    return execute_query("SELECT * FROM users", fetch=True, dictionary=True)


@router.get("/reminders/{user_id}")
def get_reminders(user_id: int):
    return execute_query(
        "SELECT * FROM reminders WHERE user_id=%s",
        (user_id,)
    )
@router.get("/status/{robot_id}")
def robot_status(robot_id: int):

    return RobotService.get_status(
        robot_id
    )


@router.get("/conversations/{user_id}")
def get_conversations(user_id: int):

    return {
        "user_id": user_id,
        "history":
            ConversationService.get_history(
                user_id
            )
    }

@router.get("/analytics/conversations/{user_id}")
def conversation_analytics(user_id: int):

    return ConversationService.get_analytics(
        user_id
    )

@router.get("/profile/{user_id}")
def get_profile(user_id: int, user=Depends(get_current_user)):
    if user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")