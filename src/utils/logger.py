import os
import logging
from logging.handlers import RotatingFileHandler
from config.settings import settings


def get_logger():
    log_file_path = os.path.join(settings.WRK_DIR, "logs", "automation.log")

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)  # Set the logging level to DEBUG

    # File Handler
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024*1024*5, backupCount=5, encoding="utf-8")
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)  # Set the logging level to DEBUG
    logger.addHandler(file_handler)

    # Console Handler
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)  # Set the console logging level to INFO
    logger.addHandler(console_handler)
    return logger


logger = get_logger()
