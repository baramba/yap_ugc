import uuid
from datetime import timedelta

from models.basemodel import BaseApiModel


class FilmLasttime(BaseApiModel):
    user_id: uuid.UUID
    film_id: uuid.UUID
    lasttime: timedelta
