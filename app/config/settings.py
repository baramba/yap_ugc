import logging
import os
from logging.config import dictConfig
from socket import gethostname

from config.logger import loggingConf
from pydantic import AnyUrl, BaseSettings, Field, KafkaDsn

# Применяем настройки логирования
dictConfig(loggingConf.dict())
log: logging.Logger = logging.getLogger("ucg.{0}".format(__name__))


class Settings(BaseSettings):
    PROJECT_NAME: str = Field(default="YAP_UGC")
    KAFKA_URL: KafkaDsn = Field(default="kafka://localhost:9092")
    KAFKA_CLIENT_ID: str = Field(default_factory=gethostname)
    KAFKA_FILM_LASTTIME_TOPIC_NAME: str = Field(default="USER_FILM_LASTTIME")

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    AUTH_SERVER_URL: AnyUrl = Field(
        default="http://localhost:5000/api/v1/users/permissions", env="AUTH_SERVER_URL"
    )

    class Config:
        env_prefix = "UGC_"


settings = Settings()
