from database.db_utils import execute_query


class ReminderManager:

    def __init__(self, user_id):

        self.user_id = user_id

    # =========================
    # ➕ CREATE REMINDER
    # =========================

    def create_reminder(
        self,
        title,
        message,
        remind_at,
        category="General",
        priority="MEDIUM",
        recurrence=None
    ):

        query = """
            INSERT INTO reminders
            (
                user_id,
                title,
                message,
                category,
                priority,
                remind_at,
                recurrence,
                status
            )
            VALUES
            (%s,%s,%s,%s,%s,%s,%s,'PENDING')
        """

        execute_query(
            query,
            (
                self.user_id,
                title,
                message,
                category,
                priority,
                remind_at,
                recurrence
            )
        )

        return {
            "status": "success",
            "message": "Reminder created"
        }

    # =========================
    # 📥 FETCH REMINDERS
    # =========================

    def get_reminders(self):

        query = """
            SELECT *
            FROM reminders
            WHERE user_id=%s
            ORDER BY remind_at ASC
        """

        return execute_query(
            query,
            (self.user_id,),
            fetch=True,
            dictionary=True
        )

    # =========================
    # 📅 TODAY REMINDERS
    # =========================

    def get_today_reminders(self):

        query = """
            SELECT *
            FROM reminders
            WHERE user_id=%s
            AND DATE(remind_at)=CURDATE()
            ORDER BY remind_at ASC
        """

        return execute_query(
            query,
            (self.user_id,),
            fetch=True,
            dictionary=True
        )

    # =========================
    # ✅ MARK DONE
    # =========================

    def mark_done(self, reminder_id):

        query = """
            UPDATE reminders
            SET
                status='DONE',
                completed_at=NOW()
            WHERE reminder_id=%s
            AND user_id=%s
        """

        execute_query(
            query,
            (
                reminder_id,
                self.user_id
            )
        )

        return {
            "status": "success"
        }

    # =========================
    # 😴 SNOOZE
    # =========================

    def snooze_reminder(
        self,
        reminder_id,
        snooze_time
    ):

        query = """
            UPDATE reminders
            SET
                status='SNOOZED',
                snoozed_until=%s
            WHERE reminder_id=%s
            AND user_id=%s
        """

        execute_query(
            query,
            (
                snooze_time,
                reminder_id,
                self.user_id
            )
        )

        return {
            "status": "success"
        }

    # =========================
    # 🗑 DELETE
    # =========================

    def delete_reminder(
        self,
        reminder_id
    ):

        query = """
            DELETE FROM reminders
            WHERE reminder_id=%s
            AND user_id=%s
        """

        execute_query(
            query,
            (
                reminder_id,
                self.user_id
            )
        )

        return {
            "status": "success"
        }