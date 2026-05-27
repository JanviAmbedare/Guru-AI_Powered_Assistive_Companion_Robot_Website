import os
import time


class CleanupService:


    @staticmethod
    def cleanup_temp_files(
        directory,
        max_age_hours=24
    ):

        now = time.time()

        for filename in os.listdir(directory):

            path = os.path.join(
                directory,
                filename
            )

            if os.path.isfile(path):

                age = (
                    now -
                    os.path.getmtime(path)
                )

                if age > (
                    max_age_hours * 3600
                ):

                    os.remove(path)