from services.command_service import RobotCommandService


class RobotService:

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
