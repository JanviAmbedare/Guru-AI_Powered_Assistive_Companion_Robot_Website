from sentence_transformers import SentenceTransformer

class ModelManager:

    embedding_model = None

    @staticmethod
    def load_models():

        if ModelManager.embedding_model is None:

            print("Loading embedding model...")

            ModelManager.embedding_model = (
                SentenceTransformer(
                    "all-MiniLM-L6-v2"
                )
            )

            print("Embedding model loaded.")