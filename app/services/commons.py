import uuid
from abc import ABC, abstractmethod
from datetime import timedelta

from pydantic import BaseModel


class BrokerMessage(BaseModel):
    user_id: uuid.UUID = None
    film_id: uuid.UUID = None
    lasttime: timedelta = None


class BrokerResponce(BaseModel):
    user_id: uuid.UUID


class BaseBrokerProducer(ABC):
    @abstractmethod
    async def push(topic: str, msg: dict) -> None:
        pass
