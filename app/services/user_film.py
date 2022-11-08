import logging
from functools import lru_cache

from aiokafka import AIOKafkaProducer
from db.kafka import get_kafka_producer
from fastapi.params import Depends
from services.commons import FilmLasttime

log: logging.Logger = logging.getLogger("ucg.{0}".format(__name__))


class UserFilmEventsService:
    def __init__(self, producer) -> None:
        self.producer: AIOKafkaProducer = producer

    async def put_film_lasttime(self, event: FilmLasttime) -> None:
        key: bytes = "{0}:{1}".format(event.user_id, event.film_id).encode()
        value: bytes = event.json().encode()
        try:
            await self.producer.send_and_wait(
                topic="user_films_lasttime", key=key, value=value
            )
        finally:
            await self.producer.stop()

        log.info("Event key: {0}, value: {1}".format(key, value))


@lru_cache(maxsize=128)
def get_user_film_event_service(
    producer: AIOKafkaProducer = Depends(get_kafka_producer),  # type: ignore
) -> UserFilmEventsService:
    return UserFilmEventsService(producer)
