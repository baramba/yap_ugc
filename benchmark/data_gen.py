#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @created: 04.11.2022
# @author: Aleksey Komissarov & baramba
# @contact: ad3002@gmail.com


import logging
import uuid
from datetime import datetime
from datetime import datetime as dt
from random import randint

from faker import Faker

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)


def generate_data(
    task_id: int,
    movies_size=100000,
    bookm_size=1000000,
):
    """Generate requeired data for tests."""

    fake = Faker("en_US")
    start: dt = dt.now()
    movies: list = []
    # bookmarks: set = set()

    for _ in range(movies_size):

        movie = dict(
            movie_id=str(uuid.uuid4()),
            title=fake.text(randint(7, 35)),
            likes=randint(0, 100),
            rating=randint(0, 10),
            year=int(fake.year()),
            created_at=datetime.utcnow(),
        )
        movies.append(movie)

    log.debug("Finished data_gen [{0}]. Elapsed: {1}".format(task_id, dt.now() - start))

    return movies
