from backend.database.db_utils import execute_query
from sentence_transformers import SentenceTransformer
from backend.models.model_manager import ModelManager
import numpy as np



class ContextMemoryService:

    @staticmethod
    def create_embedding(text):

        vector = (
            ModelManager.embedding_model
            .encode(text)
        )

        return vector.tolist()

    @staticmethod
    def save_memory(
        user_id,
        conversation_id,
        text
    ):

        embedding = (
            ContextMemoryService
            .create_embedding(text)
        )

        execute_query("""
            INSERT INTO memory_embeddings
            (
                user_id,
                conversation_id,
                summary,
                embedding
            )
            VALUES (%s,%s,%s,%s)
        """, (
            user_id,
            conversation_id,
            text,
            str(embedding)
        ))

    @staticmethod
    def search_similar_memories(
        user_id,
        current_text,
        limit=5
    ):

        current_vector = np.array(
            ContextMemoryService
            .create_embedding(current_text)
        )

        memories = execute_query("""
            SELECT *
            FROM memory_embeddings
            WHERE user_id=%s
        """, (
            user_id,
        ), fetch=True, dictionary=True)

        scored = []

        for m in memories:

            try:
                vec = np.array(
                    eval(m["embedding"])
                )

                similarity = np.dot(
                    current_vector,
                    vec
                ) / (
                    np.linalg.norm(current_vector)
                    * np.linalg.norm(vec)
                )

                scored.append({
                    "memory": m,
                    "score": float(similarity)
                })

            except:
                pass

        scored.sort(
            key=lambda x: x["score"],
            reverse=True
        )

        return scored[:limit]

class MemoryDecayService:

    @staticmethod
    def decay():

        execute_query("""

            UPDATE memory_embeddings

            SET importance_score =
            importance_score * 0.95

            WHERE importance_score > 0.1

        """)

    @staticmethod
    def reinforce(memory_id):

        execute_query("""

            UPDATE memory_embeddings

            SET importance_score =
            importance_score + 0.2

            WHERE id=%s

        """,(memory_id,))