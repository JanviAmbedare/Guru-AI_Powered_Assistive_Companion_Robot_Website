from fastapi import APIRouter, HTTPException, Depends
from database.db_connection import get_connection
from utils.dependencies import require_role, get_current_user
from database.db_utils import execute_query
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


@router.get("/conversations/{user_id}")
def get_conversations(user_id: int):
    return execute_query(
        "SELECT * FROM conversations WHERE user_id=%s ORDER BY timestamp DESC",
        (user_id,)
    )

@router.get("/profile/{user_id}")
def get_profile(user_id: int, user=Depends(get_current_user)):
    if user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not allowed")