FROM node:16 AS install

WORKDIR /usr/src/app

COPY package.json ./

RUN npm install


FROM install AS build

COPY . .

RUN npm run-script build