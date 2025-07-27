import logging
from uvicorn.config import LOGGING_CONFIG
from logging.config import dictConfig

log_config = LOGGING_CONFIG.copy()

log_config["formatters"]["turtle_chat_api"] = {
    "()": "uvicorn.logging.DefaultFormatter",
    "fmt": "%(levelprefix)s %(asctime)s.%(msecs)03d - %(message)s",
    "datefmt": "%Y-%m-%d %H:%M:%S",
}
log_config["handlers"]["turtle_chat_api"] = {
    "formatter": "turtle_chat_api",
    "class": "logging.StreamHandler",
    "stream": "ext://sys.stdout",
}
log_config["loggers"]["turtle_chat_api"] = {
    "handlers": ["turtle_chat_api"],
    "level": "INFO",
}

dictConfig(log_config)

logger = logging.getLogger("turtle_chat_api")
