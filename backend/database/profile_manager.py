from backend.database.db_utils import execute_query
import json

class UserProfileManager:

    def __init__(self, user_id):
        self.user_id = user_id

    def create_profile(self, name, preferences=None, health_info=None):

        # 🚫 check if profile already exists
        existing = execute_query(
            "SELECT * FROM user_profiles WHERE user_id=%s",
            (self.user_id,),
            fetch_one=True,
            dictionary=True
        )

        if existing:
            raise Exception("Profile already exists")

        query = """
        INSERT INTO user_profiles (user_id, name, preferences, health_info)
        VALUES (%s, %s, %s, %s)
        """

        execute_query(query, (
            self.user_id,
            name,
            json.dumps(preferences or {}),
            json.dumps(health_info or {})
        ))

        return {"status": "created"}

    def get_profile(self):
        query = "SELECT * FROM user_profiles WHERE user_id=%s"

        result = execute_query(
            query,
            (self.user_id,),
            fetch_one=True,
            dictionary=True
        )

        if result:
            result["preferences"] = json.loads(result["preferences"] or "{}")
            result["health_info"] = json.loads(result["health_info"] or "{}")

        return result

    def update_profile(self, preferences=None, health_info=None):

        query = """
        UPDATE user_profiles
        SET preferences=%s, health_info=%s
        WHERE user_id=%s
        """

        execute_query(query, (
            json.dumps(preferences or {}),
            json.dumps(health_info or {}),
            self.user_id
        ))

        return {"status": "updated"}

    def delete_profile(self):
        query = "DELETE FROM user_profiles WHERE user_id=%s"
        execute_query(query, (self.user_id,))
        return {"status": "deleted"}