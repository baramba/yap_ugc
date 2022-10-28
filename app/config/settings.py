import logging
import os
from logging.config import dictConfig
from socket import gethostname

from app.config.logger import loggingConf
from pydantic import AnyUrl, BaseSettings, Field, KafkaDsn

# Применяем настройки логирования
dictConfig(loggingConf.dict())
log = logging.getLogger("ucg.{0}".format(__name__))
log.info("Логирование настроено")


class Settings(BaseSettings):
    # Название сервиса
    PROJECT_NAME: str = Field(default="YAP_UGC")
    KAFKA_URL: KafkaDsn = Field(default="kafka://localhost:9092")
    KAFKA_CLIENT_ID: str = Field(default_factory=gethostname)
    KAFKA_FILM_LASTTIME_TOPIC_NAME: str = Field(default="USER_FILM_LASTTIME")
    # # Настройки Redis
    # REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
    # REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
    # REDIS_PROTO = os.getenv("REDIS_PROTO", "redis")
    # # redis://[[username]:[password]]@localhost:6379/0
    # REDIS_URL = "{0}://{1}:{2}".format(REDIS_PROTO, REDIS_HOST, REDIS_PORT)

    # # Настройки Elasticsearch
    # ELASTIC_PROTO = os.getenv("ELASTIC_PROTO", "http")
    # ELASTIC_HOST = os.getenv("ELASTIC_HOST", "127.0.0.1")
    # ELASTIC_PORT = int(os.getenv("ELASTIC_PORT", 9200))
    # ELASTIC_URL = "{0}://{1}:{2}".format(ELASTIC_PROTO, ELASTIC_HOST, ELASTIC_PORT)

    # Корень проекта
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    AUTH_SERVER_URL: AnyUrl = Field(
        default="http://localhost:5000/api/v1/users/permissions", env="AUTH_SERVER_URL"
    )

    class Config:
        env_prefix = "UGC_"


settings = Settings()
