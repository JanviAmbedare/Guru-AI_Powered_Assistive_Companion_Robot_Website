import requests


class AIClient:


    BASE_URL = (
        "http://localhost:9000"
    )


    @staticmethod
    def generate_face_embeddings(
        user_id
    ):

        return requests.post(

            f"{AIClient.BASE_URL}/face/train",

            json={
                "user_id": user_id
            }
        ).json()


    @staticmethod
    def generate_voice_embeddings(
        user_id
    ):

        return requests.post(

            f"{AIClient.BASE_URL}/voice/train",

            json={
                "user_id": user_id
            }
        ).json()