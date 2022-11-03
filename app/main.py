import logging

import uvicorn
from api.v1 import user_events
from config.settings import settings
from db import kafka
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from kafka import KafkaProducer

log: logging.Logger = logging.getLogger("ucg.{0}".format(__name__))

description: str = """
# Сервис
yap_ugc помогает сохранять различные события для последующего нализа.

## Реализованные типы событий:
  - Временная метка последнего места просмотра фильма

"""

tags_metadata = [
    {
        "name": "films",
        "description": "События, связанные с фильмами.",
    },
    {
        "name": "about",
        "description": "Информация о сервисе.",
    },
]

app: FastAPI = FastAPI(
    title=settings.PROJECT_NAME,
    description=description,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    openapi_tags=tags_metadata,
)


@app.on_event("startup")
async def startup() -> None:

    kafka.producer = KafkaProducer(
        bootstrap_servers=[
            "{0}:{1}".format(settings.KAFKA_URL.host, settings.KAFKA_URL.port),
        ],
        client_id=settings.KAFKA_CLIENT_ID,
    )


@app.on_event("shutdown")
async def shutdown() -> None:
    if kafka.producer:
        kafka.producer.flush()
        kafka.producer.close()


@app.get("/", tags=["about"])
async def root():
    return {
        "message": {
            "Project": settings.PROJECT_NAME,
            "Path": settings.BASE_DIR,
        }
    }


app.include_router(user_events.router, prefix="/api/v1/films", tags=["films"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
    )
