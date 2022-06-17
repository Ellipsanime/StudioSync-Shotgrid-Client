import logging
import sys
from functools import lru_cache


_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(format=_FORMAT, level=logging.INFO)


@lru_cache
def global_logger() -> logging.Logger:
    logging.basicConfig(format=_FORMAT, level=logging.INFO)
    logger = logging.getLogger("global")
    logger.setLevel(logging.INFO)
    return logger


def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_FORMAT))
    handler.setLevel(logging.DEBUG)
    logger.handlers = []
    logger.addHandler(handler)
    return logger
