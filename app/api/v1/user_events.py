from fastapi.exceptions import HTTPException
from fastapi.param_functions import Query
from fastapi.params import Depends
from fastapi.requests import Request
from fastapi.routing import APIRouter

from app.models.user_events import MovieLasttime

router = APIRouter()


@router.post("/movie/lasttime")
async def user_movie_lasttime(lastime: MovieLasttime):
    pass
