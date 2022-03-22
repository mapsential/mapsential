FROM node:17

WORKDIR /usr/src/app

COPY . .

RUN npm install

ENTRYPOINT npm run start-docker-dev