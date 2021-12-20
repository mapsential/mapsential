FROM node:18 AS install

COPY ./package.json .
# Copying yarn.lock ensures (version) pinned dependencies
COPY ./yarn.lock .

RUN yarn install


FROM install AS run

COPY ./index.js .

ENTRYPOINT node index.js