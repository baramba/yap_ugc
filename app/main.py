import logging

import uvicorn
from fastapi import FastAPI
from kafka import KafkaProducer

from app.api.v1 import user_events
from app.config.settings import settings
from app.db import kafka

log = logging.getLogger("ucg.{0}".format(__name__))


log.info("Инициализация приложения")

app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    # docs_url="/api/openapi",
    # openapi_url="/api/openapi.json",
    # default_response_class=ORJSONResponse,
)


@app.on_event("startup")
async def startup() -> None:

    kafka.producer = KafkaProducer(
        bootstrap_servers=[
            "{0}:{1}".format("localhost", "9092"),
        ],
        client_id=settings.KAFKA_CLIENT_ID,
    )


@app.on_event("shutdown")
async def shutdown() -> None:
    kafka.producer.flush()
    kafka.producer.close()


@app.get("/")
async def root():
    def on_send_success(record_meta):
        log.debug(record_meta.topic)
        log.debug(record_meta.partition)
        log.debug(record_meta.offset)

    def on_send_error(excp):
        log.error("I am an errback", exc_info=excp)

    future = (
        kafka.producer.send("user_films_lasttime", key=b"key", value=b"value")
        .add_callback(on_send_success)
        .add_errback(on_send_error)
    )
    future.get(1)
    return {
        "message": {
            "Project": settings.PROJECT_NAME,
            "Path": settings.BASE_DIR,
        }
    }


app.include_router(user_events.router, prefix="/api/v1/user", tags=["user events"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
    )
