#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#@created: 04.11.2022
#@author: Aleksey Komissarov & baramba
#@contact: ad3002@gmail.com 


import uuid
from datetime import datetime
from random import randint
from typing import Any
from faker import Faker


def generate_data(movies_size=100000, bookm_size=1000000) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    ''' Generate requeired data for tests.
    '''
    
    fake = Faker()
    
    movies: list = []
    bookmarks: set = set()

    for _ in range(movies_size):

        movie = dict(
            movie_id=str(uuid.uuid4()),
            title=fake.text(randint(7, 35)),
            likes=randint(0, 100),
            rating=randint(0, 10),
            year=int(fake.year()),
            created_at=datetime.utcnow()
        )

        for _ in range(randint(1, 10)):
            if len(bookmarks) > bookm_size:
                break
            bookmark = dict(
                user_id=randint(1, 25),
                movie_id=movie['movie_id'],
                created_at=datetime.utcnow()
            )
            bookmarks.add(bookmark)

        movies.append(movie)

    return movies, list(bookmarks)
