import uuid
from datetime import datetime, timedelta

from models.basemodel import BaseApiModel
from pydantic import Field


class FilmLasttime(BaseApiModel):
    user_id: uuid.UUID
    film_id: uuid.UUID
    lasttime: timedelta
    event_time: datetime = Field(default_factory=datetime.now)

    class Config:
        json_encoders = {
            datetime: lambda v: "{0}".format(v.timestamp()),
        }
