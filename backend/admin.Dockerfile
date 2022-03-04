FROM python:3.10 AS install

RUN pip install pipenv

WORKDIR /usr/src/backend

COPY ./backend/Pipfile /usr/src/backend/Pipfile
COPY ./backend/Pipfile.lock /usr/src/backend/Pipfile.lock

RUN pipenv install --system --deploy


FROM install AS run

ENV ENV=prod

ENTRYPOINT cd backend \
    # Uncomment following and run `podman-compose down && podman-compose build && podman-compose up`
    # if migrations should be run.
    # && piccolo migrations forwards all \
    && gunicorn -w 1 -k uvicorn.workers.UvicornWorker app:app -b 0.0.0.0:8090
