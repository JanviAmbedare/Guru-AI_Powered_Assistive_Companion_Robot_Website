class QueueService:

    @staticmethod
    def add_job(
        job_type,
        data
    ):

        print(
            f"QUEUE JOB: {job_type}"
        )

        return True