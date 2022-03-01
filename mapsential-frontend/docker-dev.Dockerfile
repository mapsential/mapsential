FROM node:17

WORKDIR /usr/src/app

ENV REACT_APP_IS_DOCKER_DEV=true

ENTRYPOINT npm start