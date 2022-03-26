FROM node:17 AS install

RUN npm install -g serve


FROM install AS serve

WORKDIR /usr/src/app

COPY build ./build

ENTRYPOINT serve -s build -l 8100