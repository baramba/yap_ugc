import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default) -> str:
    return orjson.dumps(v, default=default).decode()


class BaseApiModel(BaseModel):
    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps
