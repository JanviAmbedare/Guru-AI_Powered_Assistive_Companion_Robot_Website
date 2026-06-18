import requests
import os

AI_SERVICE_URL = os.getenv("AI_SERVICE_URL")


class AIClient:

    API_PREFIX = "/api"

    @staticmethod
    def chat(user_id: int, message: str):

        response = requests.post(
            f"{AI_SERVICE_URL}{AIClient.API_PREFIX}/chat",
            json={
                "user_id": user_id,
                "message": message
            },
            timeout=60
        )

        response.raise_for_status()
        return response.json()
    @staticmethod
    def get_training_status(user_id):

        response = requests.get(
            f"{AI_SERVICE_URL}/training/status/{user_id}",
            timeout=30
        )

        response.raise_for_status()

        return response.json()
    # @staticmethod
    # def verify_face(file):

    #     response = requests.post(
    #         f"{AI_SERVICE_URL}{AIClient.API_PREFIX}/face/verify",
    #         files={"file": file},
    #         timeout=60
    #     )

    #     response.raise_for_status()
    #     return response.json()

    # @staticmethod
    # def verify_voice(file):

    #     response = requests.post(
    #         f"{AI_SERVICE_URL}{AIClient.API_PREFIX}/voice/verify",
    #         files={"file": file},
    #         timeout=60
    #     )

    #     response.raise_for_status()
    #     return response.json()

    # @staticmethod
    # def train_face(user_id):

    #     response = requests.post(
    #         f"{AI_SERVICE_URL}{AIClient.API_PREFIX}/training/face/{user_id}",
    #         timeout=300
    #     )

    #     response.raise_for_status()
    #     return response.json()

    # @staticmethod
    # def train_voice(user_id):

    #     response = requests.post(
    #         f"{AI_SERVICE_URL}{AIClient.API_PREFIX}/training/voice/{user_id}",
    #         timeout=300
    #     )

    #     response.raise_for_status()
    #     return response.json()