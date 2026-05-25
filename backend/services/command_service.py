import socket
import json


class RobotCommandService:

    ROBOT_IP = "192.168.1.10"
    ROBOT_PORT = 5050

    @staticmethod
    def send_command(command, payload=None):

        data = {
            "command": command,
            "payload": payload or {}
        }

        try:

            client = socket.socket(
                socket.AF_INET,
                socket.SOCK_STREAM
            )

            client.connect((
                RobotCommandService.ROBOT_IP,
                RobotCommandService.ROBOT_PORT
            ))

            client.send(
                json.dumps(data).encode()
            )

            response = client.recv(4096).decode()

            client.close()

            return {
                "status": "success",
                "response": response
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }