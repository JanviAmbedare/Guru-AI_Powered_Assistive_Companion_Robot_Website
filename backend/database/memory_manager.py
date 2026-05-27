from database.db_utils import execute_query

class MemoryManager:

    def __init__(self, user_id):
        self.user_id = user_id

    def save_conversation(self, text, intent, response, sentiment):
        query = """
        INSERT INTO conversations (user_id, text, intent, response, sentiment)
        VALUES (%s, %s, %s, %s, %s)
        """
        execute_query(query, (self.user_id, text, intent, response, sentiment))
        return {"status": "saved"}

    def get_recent_context(self, limit=5):
        query = """
        SELECT * FROM conversations
        WHERE user_id=%s ORDER BY timestamp DESC LIMIT %s
        """
        data = execute_query(query, (self.user_id, limit), fetch=True, dictionary=True)
        return data[::-1]

    def update_last_response(self, new_response):
        query = """
        UPDATE conversations
        SET response=%s
        WHERE id = (
            SELECT id FROM (
                SELECT id FROM conversations
                WHERE user_id=%s
                ORDER BY timestamp DESC LIMIT 1
            ) temp
        )
        """
        execute_query(query, (new_response, self.user_id))
        return {"status": "updated"}

    def delete_old_conversations(self, limit=50):
        query = """
        DELETE FROM conversations
        WHERE id IN (
            SELECT id FROM (
                SELECT id FROM conversations
                WHERE user_id=%s
                ORDER BY timestamp ASC LIMIT %s
            ) temp
        )
        """
        execute_query(query, (self.user_id, limit))
        return {"status": "deleted"}