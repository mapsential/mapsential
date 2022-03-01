FROM python:3.10 AS install

RUN pip install pipenv

WORKDIR /usr/src/admin-backend

# Copying means that this build stage cannot be cached.
# TODO: Find a way to cache build stage.
COPY ./admin-backend /usr/src/admin-backend
COPY ./db /usr/src/db

RUN pipenv install --system --deploy


FROM install AS run

EXPOSE 80

ENV ENV=prod

ENTRYPOINT cd admin_backend \
    # Uncomment following and run `podman-compose down && podman-compose build && podman-compose up`
    # if migrations should be run.
    # && piccolo migrations forwards all \
    && gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app -b 0.0.0.0:8090
