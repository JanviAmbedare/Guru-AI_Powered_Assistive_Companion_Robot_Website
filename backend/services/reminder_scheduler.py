import time
import schedule
import threading


from database.db_utils import (    execute_query)
from services.alert_service import (    AlertService)
from services.robot_service import (    RobotService)
from services.notification_service import (    NotificationService)
from services.logging_service import (    LoggingService)


class ReminderScheduler:

    # =========================
    # 🔍 CHECK REMINDERS
    # =========================

    @staticmethod
    def check_reminders():

        print(
            "🔍 Checking reminders..."
        )

        reminders = execute_query("""

            SELECT *
            FROM reminders
            WHERE
                status='PENDING'
            AND
                remind_at <= NOW()

        """, fetch=True, dictionary=True)

        print(reminders)

        for reminder in reminders:

            try:

                message = (
                    f"Reminder: "
                    f"{reminder['message']}"
                )

                print(
                    "🔔 TRIGGERING:",
                    message
                )

                # =========================
                # 👤 USER DATA
                # =========================

                user = execute_query("""

                        SELECT
                            phone_number
                        FROM users
                        WHERE id=%s

                    """, (

                        reminder["user_id"],

                    ), fetch_one=True,
                    dictionary=True)

                phone = None

                if user:

                        phone = user.get(
                            "phone_number"
                        )

                # =========================
                # 🚨 CREATE ALERT
                # =========================

                AlertService.create_alert(

                    user_id=
                        reminder["user_id"],

                    title=
                        "Reminder Triggered",

                    message=message,

                    alert_type="INFO",

                    severity="LOW",

                    source=
                        "REMINDER_SYSTEM"
                )

                # =========================
                # 🤖 ROBOT SPEAK
                # =========================

                try:

                    threading.Thread(

                        target=
                            RobotService.speak,

                        args=(message,),

                        daemon=True

                    ).start()

                except Exception as e:

                    print(
                        "Robot error:",
                        e
                    )

                # =========================
                # 🔔 NOTIFICATIONS
                # =========================

                NotificationService.send_all(

                    whatsapp_to=phone,

                    title="GURU Reminder",

                    message=message
                )

                # =========================
                # ✅ MARK DONE
                # =========================

                execute_query("""

                    UPDATE reminders
                    SET status='DONE'
                    WHERE reminder_id=%s

                """, (

                    reminder["reminder_id"],

                ))

                LoggingService.info(
                    f"Reminder completed: "
                    f"{reminder['title']}"
                )

            except Exception as e:

                print(
                    "Reminder Trigger Error:",
                    e
                )

                LoggingService.error(
                    str(e)
                )

    # =========================
    # 🚀 START SCHEDULER
    # =========================

    @staticmethod
    def start():

        schedule.every(10).seconds.do(

            ReminderScheduler
            .check_reminders
        )

        print(
            "⏰ Reminder scheduler started"
        )

        while True:

            schedule.run_pending()

            time.sleep(1)