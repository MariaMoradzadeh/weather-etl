import logging
import sys


def get_logger(name: str = "weather_etl") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger  # prevent duplicate handlers

    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")
    handler.setFormatter(fmt)
    logger.addHandler(handler)
    return logger
