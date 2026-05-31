from services.command_service import RobotCommandService
from database.db_connection import get_connection

class RobotService:
    @staticmethod
    def get_status(robot_id: int):

        conn = get_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT
                temperature,
                battery_level,
                obstacle_detected,
                location,
                timestamp
            FROM sensor_data
            WHERE robot_id=%s
            ORDER BY timestamp DESC
            LIMIT 1
        """, (robot_id,))

        status = cursor.fetchone()

        cursor.close()
        conn.close()

        return status
    @staticmethod
    def get_telemetry(
        robot_id: int,
        limit: int = 100
    ):

        conn = get_connection()

        cursor = conn.cursor(
            dictionary=True
        )

        cursor.execute("""
            SELECT
                battery_level,
                temperature,
                obstacle_detected,
                location,
                timestamp
            FROM sensor_data
            WHERE robot_id=%s
            ORDER BY timestamp DESC
            LIMIT %s
        """, (robot_id, limit))

        rows = cursor.fetchall()

        cursor.close()
        conn.close()

        return rows

    @staticmethod
    def move_forward():
        return RobotCommandService.send_command(
            "MOVE_FORWARD"
        )

    @staticmethod
    def stop():
        return RobotCommandService.send_command(
            "STOP"
        )

    @staticmethod
    def speak(text):
        return RobotCommandService.send_command(
            "SPEAK",
            {"text": text}
        )

    @staticmethod
    def battery_status():
        return RobotCommandService.send_command(
            "BATTERY_STATUS"
        )
