from fastapi import APIRouter, HTTPException, Depends
from database.db_connection import get_connection
from utils.dependencies import require_role, get_current_user

router = APIRouter()

def execute_query(query, params=None):
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query, params or ())
        data = cursor.fetchall()

        return data

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        cursor.close()
        conn.close()


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