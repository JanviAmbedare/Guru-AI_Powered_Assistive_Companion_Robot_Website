import logging


logging.basicConfig(
    filename="guru.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class LoggingService:

    @staticmethod
    def info(message):
        logging.info(message)

    @staticmethod
    def error(message):
        logging.error(message)

    @staticmethod
    def warning(message):
        logging.warning(message)