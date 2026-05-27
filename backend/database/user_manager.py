from database.db_utils import execute_query

class UserManager:

    def create_user(self, name, role, password, disability_type=None, language_pref=None):
        # 🔐 normalize role
        role = role.upper()

        # 🚫 prevent duplicate user
        existing = execute_query(
            """
        SELECT id
        FROM users
        WHERE name=%s
        """,
            (name,),
            fetch_one=True,
            dictionary=True
        )

        if existing:
            raise Exception("User already exists")

        # ✅ insert user
        query = """
        INSERT INTO users (name, role, password, disability_type, language_pref)
        VALUES (%s, %s, %s, %s, %s)
        """
        result = execute_query(query, (name, role, password, disability_type, language_pref), return_last_id=True)

        return int(result)


    def get_user_by_name(self, name):
        user = execute_query(
            "SELECT * FROM users WHERE name=%s",
            (name,),
            fetch_one=True,
            dictionary=True
        )
        return user


class BehaviorLearningService:

    @staticmethod
    def analyze_patterns(user_id):

        data = execute_query("""
            SELECT *
            FROM conversations
            WHERE user_id=%s
        """,(user_id,),
        fetch=True,
        dictionary=True)

        late_night_usage = 0

        for d in data:

            hour = d["timestamp"].hour

            if hour >= 23 or hour <= 4:
                late_night_usage += 1

        if late_night_usage > 10:

            execute_query("""
                INSERT INTO user_behavior_patterns
                (
                    user_id,
                    behavior_type,
                    pattern_data,
                    confidence
                )
                VALUES (%s,%s,%s,%s)
            """,(
                user_id,
                "sleep_pattern",
                "User frequently active late night",
                0.89
            ))