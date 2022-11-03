import logging

from fastapi.params import Depends
from fastapi.routing import APIRouter
from models.user_events import FilmLasttime as FilmLasttimeApi
from services.commons import FilmLasttime
from services.user_film import UserFilmEventsService, get_user_film_event_service

router: APIRouter = APIRouter()

log: logging.Logger = logging.getLogger("ucg.{0}".format(__name__))


@router.post(
    "/lasttime",
    name="Последний раз",
    description="Сохранение метки о просмотре фильма.",
)
async def film_lasttime(
    event: FilmLasttimeApi,
    user_film_event_service: UserFilmEventsService = Depends(
        get_user_film_event_service
    ),  # type: ignore
) -> None:

    log.debug("Event: {0}".format(event))

    await user_film_event_service.put_film_lasttime(
        FilmLasttime(
            user_id=event.user_id,
            film_id=event.film_id,
            lasttime=event.lasttime,
        )
    )
