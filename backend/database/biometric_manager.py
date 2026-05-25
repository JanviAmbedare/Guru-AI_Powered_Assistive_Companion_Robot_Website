from datetime import datetime

from backend.database.db_utils import execute_query


class BiometricManager:

    # =========================
    # 🏷️ GENERATE LABEL
    # =========================

    def generate_label(
        self,
        user_id,
        bio_type
    ):

        bio_type = bio_type.upper()

        return (
            f"user_{user_id}_"
            f"{bio_type.lower()}_v1"
        )

    # =========================
    # 💾 SAVE BIOMETRIC
    # =========================

    def save_biometric(
        self,
        user_id,
        bio_type,
        file_path,
        sample_number=0,
        quality_score=0.0
    ):

        label = self.generate_label(
            user_id,
            bio_type
        )

        query = """
        INSERT INTO biometric_profiles
        (
            user_id,
            type,
            label,
            file_path,
            embedding_path,
            created_at,
            sample_number,
            is_trained,
            model_version,
            quality_score
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s,
            %s
        )
        """

        execute_query(
            query,
            (
                user_id,
                bio_type.upper(),
                label,
                file_path,
                None,
                datetime.now(),
                sample_number,
                False,
                "v1",
                quality_score
            )
        )

        return {
            "status": "success",
            "label": label,
            "message": (
                f"{bio_type} "
                "biometric saved"
            )
        }

    # =========================
    # 🧠 SAVE EMBEDDING
    # =========================

    def save_embedding_path(
        self,
        user_id,
        bio_type,
        embedding_path
    ):

        query = """
        UPDATE biometric_profiles
        SET embedding_path=%s
        WHERE user_id=%s
        AND type=%s
        """

        execute_query(
            query,
            (
                embedding_path,
                user_id,
                bio_type.upper()
            )
        )

        return {
            "status": "success"
        }

    # =========================
    # 🤖 MARK TRAINED
    # =========================

    def mark_model_trained(
        self,
        user_id,
        bio_type,
        model_version="v1"
    ):

        query = """
        UPDATE biometric_profiles
        SET
            is_trained=%s,
            model_version=%s
        WHERE user_id=%s
        AND type=%s
        """

        execute_query(
            query,
            (
                True,
                model_version,
                user_id,
                bio_type.upper()
            )
        )

        return {
            "status": "success",
            "message": (
                f"{bio_type} "
                "model trained"
            )
        }

    # =========================
    # 📂 FETCH BIOMETRICS
    # =========================

    def get_user_biometrics(
        self,
        user_id
    ):

        query = """
        SELECT *
        FROM biometric_profiles
        WHERE user_id=%s
        """

        result = execute_query(
            query,
            (user_id,),
            fetch=True,
            dictionary=True
        )

        return result

    # =========================
    # 🗑️ DELETE BIOMETRIC
    # =========================

    def delete_biometric(
        self,
        user_id,
        bio_type
    ):

        query = """
        DELETE FROM biometric_profiles
        WHERE user_id=%s
        AND type=%s
        """

        execute_query(
            query,
            (
                user_id,
                bio_type.upper()
            )
        )

        return {
            "status": "success",
            "message": (
                f"{bio_type} deleted"
            )
        }