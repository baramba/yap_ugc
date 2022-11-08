import asyncio
import logging
import time
from datetime import datetime as dt
from datetime import timedelta as td
from multiprocessing import Process

from asynch import connect
from asynch.connection import Connection
from clickhouse_driver import Client
from data_gen import generate_data

ch_host: str = "localhost"
ch_port: str = "9900"

batch: int = 200000
total_size: int = 10000000
task_num: int = 10

log: logging.Logger = logging.getLogger(__name__)
log.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
log.addHandler(ch)


drop: list[str] = [
    "DROP TABLE IF EXISTS ugc_bm_movies ON CLUSTER company_cluster SYNC;",
    "DROP TABLE IF EXISTS ugc_bm_bookmarks ON CLUSTER company_cluster SYNC;",
    "DROP TABLE IF EXISTS default.ugc_bm_movies_dis ON CLUSTER company_cluster SYNC;",
    "DROP TABLE IF EXISTS default.ugc_bm_bookmarks_dis ON CLUSTER company_cluster SYNC;",
]
create: list[str] = [
    "CREATE TABLE ugc_bm_movies ON CLUSTER company_cluster (movie_id UUID, title String, likes Int16, rating Int32, year Int16, created_at DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/ugc_shard/{shard}/{table}', '{replica}') PARTITION BY year ORDER BY created_at;",
    "CREATE TABLE default.ugc_bm_movies_dis ON CLUSTER company_cluster (movie_id UUID, title String, likes Int16, rating Int32, year Int16, created_at DateTime) ENGINE = Distributed('company_cluster', '', ugc_bm_movies, rand());",
    "CREATE TABLE ugc_bm_bookmarks ON CLUSTER company_cluster (movie_id UUID, user_id UUID, created_at DateTime) Engine=ReplicatedMergeTree('/clickhouse/tables/ugc_shard/{shard}/{table}', '{replica}') ORDER BY created_at;",
    "CREATE TABLE default.ugc_bm_bookmarks_dis ON CLUSTER company_cluster (movie_id UUID, user_id UUID, created_at DateTime) ENGINE = Distributed('company_cluster', '', ugc_bm_bookmarks, rand());",
]


async def connect_database() -> Connection:
    return await connect(host="127.0.0.1", port=9900)


async def init_db() -> None:
    conn: Connection = await connect_database()
    log.info("Start init DB: {0}".format(dt.now()))
    async with conn.cursor() as cursor:
        for query in drop:
            await cursor.execute(query)
        for query in create:
            await cursor.execute(query)
    log.info("Finished init DB: {0}".format(dt.now()))


async def insert_data(task_id: int, data: list) -> None:
    conn: Connection = await connect_database()
    start: dt = dt.now()
    log.debug("Task #{0}. Started: {1}".format(task_id, start))
    async with conn.cursor() as cursor:
        await cursor.execute(
            "INSERT INTO default.ugc_bm_movies_dis (*) VALUES",
            data,
        )
        log.info(
            "Task #{0}. Finished: {1}, Elapsed: {2}".format(
                task_id, dt.now(), dt.now() - start
            )
        )


def select_time():
    query: str = "select year, rating, count()  from default.ugc_bm_movies_dis group by rating, year  order by year, rating;"
    measurements: list[float] = []
    client = Client(host=ch_host, port=ch_port)
    start: dt = dt.now()
    while (dt.now() - start) < td(seconds=30):
        client.execute(query=query)
        measurements.append(client.last_query.elapsed)
        time.sleep(1)
    log.info(
        "Select measurements: Count - {0}, Mean: {1}".format(
            len(measurements), sum(measurements) / len(measurements)
        )
    )


async def insert_data_task(data):
    # Вставка данных
    start = dt.now()
    inserted_rows: int = 0
    tasks: list = []
    task_id: int = 0
    while inserted_rows < total_size:
        for _ in range(task_num):
            tasks.append(
                asyncio.create_task(insert_data(task_id=task_id, data=data[task_id]))
            )
            task_id += 1
        await asyncio.gather(*tasks)
        inserted_rows += task_num * batch

    log.debug("Inserting data was finished. Elapsed: {0}".format(dt.now() - start))


async def main():

    start: dt = dt.now()
    data: list[list] = []

    # Инициализация БД
    await init_db()

    # Генерация данных
    for x in range(total_size // batch):
        data.append(generate_data(movies_size=batch, bookm_size=batch, task_id=0))
    log.info("Genaration data was finished. Elapsed: {0}".format(dt.now() - start))

    await insert_data_task(data)

    p: Process = Process(target=select_time)
    p.start()
    await insert_data_task(data)
    p.join()


if __name__ == "__main__":
    asyncio.run(main())
