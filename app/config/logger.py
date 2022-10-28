from pydantic import BaseModel


class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "YAP_UGC"
    LOG_FORMAT: str = "%(levelprefix)s %(asctime)s - %(name)s - %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    root = {
        "level": "INFO",
        "formatter": ["default"],
        "handlers": ["default"],
    }

    loggers = {
        "yap_ugc": {"handlers": ["default"], "level": LOG_LEVEL},
    }


loggingConf = LogConfig()
