import logging
from backend.database.db_connection import get_connection

logger = logging.getLogger(__name__)

def execute_query(query, params=None, fetch=False, fetch_one=False, dictionary=False,  return_last_id=False):
    conn = get_connection()
    cursor = conn.cursor(dictionary=dictionary)

    try:
        cursor.execute(query, params or ())

        if return_last_id:

            conn.commit()

            return cursor.lastrowid

        if fetch_one:
            return cursor.fetchone()

        if fetch:
            return cursor.fetchall()

        conn.commit()
        return {"status": "success"}

    except Exception as e:
        conn.rollback()
        logger.error(f"DB Error: {str(e)}")
        raise e

    finally:
        cursor.close()
        conn.close()