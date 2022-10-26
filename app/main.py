import uvicorn
from fastapi import FastAPI

from app.api.v1 import user_events

app = FastAPI()


@app.on_event("startup")
async def startup():
    pass
    # redis.redis = await aioredis.from_url(config.REDIS_URL)
    # elastic.es = AsyncElasticsearch(hosts=[config.ELASTIC_URL])


@app.on_event("shutdown")
async def shutdown():
    pass
    # await redis.redis.close()
    # await elastic.es.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(user_events.router, prefix="/api/v1/user", tags=["user events"])
# app.include_router(genres.router, prefix="/api/v1/genres", tags=["genre"])
# app.include_router(persons.router, prefix="/api/v1/persons", tags=["person"])


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
    )
