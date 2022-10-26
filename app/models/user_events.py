import uuid
from datetime import timedelta

from app.models.basemodel import BaseApiModel


class MovieLasttime(BaseApiModel):
    user_id: uuid.UUID
    film_id: uuid.UUID
    lasttime: timedelta
