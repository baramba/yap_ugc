FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

ARG WORKDIR=/code
ARG SRC_CODE_DIR=app
ARG POETRY_T=pyproject.toml
ARG POETRY_L=poetry.lock
ARG USER=app
ARG GROUP=apps

WORKDIR ${WORKDIR}

ENV PATH="/home/${USER}/.local/bin:${PATH}"

RUN groupadd -r ${GROUP} && useradd --no-log-init -m -r -g ${GROUP} ${USER} && \
    chown -R ${USER}:${GROUP} ${WORKDIR} \
    && chown -R ${USER}:${GROUP} /home/${USER} \
    && apt update && apt install -y build-essential && apt install -y libpq-dev && rm -rf /var/lib/apt/lists/*

USER app

RUN pip install --upgrade pip && pip install poetry==1.2

COPY --chown=${USER}:${GROUP} ./${POETRY_T} ./
COPY --chown=${USER}:${GROUP} ./${POETRY_L} ./

RUN poetry update --only main --no-ansi

COPY --chown=${USER}:${GROUP} ${SRC_CODE_DIR} ./
COPY --chown=${USER}:${GROUP} ./gunicorn.conf.py ./
COPY --chown=${USER}:${GROUP} ./entrypoint.sh ./

RUN chmod u+x ./entrypoint.sh