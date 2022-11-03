import logging
from functools import lru_cache

from db.kafka import get_kafka_producer
from fastapi.params import Depends
from kafka import KafkaProducer
from services.commons import FilmLasttime

log: logging.Logger = logging.getLogger("ucg.{0}".format(__name__))


class UserFilmEventsService:
    def __init__(self, producer) -> None:
        self.producer: KafkaProducer = producer

    async def put_film_lasttime(self, event: FilmLasttime) -> None:
        key: bytes = "{0}:{1}".format(event.user_id, event.film_id).encode()
        value: bytes = event.json().encode()
        self.producer.send(topic="user_films_lasttime", key=key, value=value)
        log.info("Event key: {0}, value: {1}".format(key, value))


@lru_cache(maxsize=128)
def get_user_film_event_service(
    producer: KafkaProducer = Depends(get_kafka_producer),  # type: ignore
) -> UserFilmEventsService:
    return UserFilmEventsService(producer)
