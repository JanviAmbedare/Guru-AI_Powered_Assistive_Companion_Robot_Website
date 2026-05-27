from fastapi import APIRouter
from database.reminder_manager import ReminderManager

router = APIRouter(
    prefix="/reminder",
    tags=["Reminders"]
)


# =========================
# ➕ CREATE
# =========================

@router.post("/")
def create_reminder(data: dict):

    rm = ReminderManager(
        data["user_id"]
    )

    return rm.create_reminder(
        title=data["title"],
        message=data["message"],
        remind_at=data["remind_at"],
        category=data.get(
            "category",
            "General"
        ),
        priority=data.get(
            "priority",
            "MEDIUM"
        ),
        recurrence=data.get(
            "recurrence"
        )
    )


# =========================
# 📥 GET ALL
# =========================

@router.get("/{user_id}")
def get_reminders(user_id: int):

    rm = ReminderManager(user_id)

    return rm.get_reminders()


# =========================
# 📅 TODAY
# =========================

@router.get("/today/{user_id}")
def today_reminders(user_id: int):

    rm = ReminderManager(user_id)

    return rm.get_today_reminders()


# =========================
# ✅ DONE
# =========================

@router.put("/done/{user_id}/{reminder_id}")
def mark_done(
    user_id: int,
    reminder_id: int
):

    rm = ReminderManager(user_id)

    return rm.mark_done(reminder_id)


# =========================
# 😴 SNOOZE
# =========================

@router.put("/snooze/{user_id}/{reminder_id}")
def snooze_reminder(
    user_id: int,
    reminder_id: int,
    snooze_time: str
):

    rm = ReminderManager(user_id)

    return rm.snooze_reminder(
        reminder_id,
        snooze_time
    )


# =========================
# 🗑 DELETE
# =========================

@router.delete("/{user_id}/{reminder_id}")
def delete_reminder(
    user_id: int,
    reminder_id: int
):

    rm = ReminderManager(user_id)

    return rm.delete_reminder(
        reminder_id
    )