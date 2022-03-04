# mapsential

## Architecture

The project is implemented as a service oriented architecture (SOA). These services are configured by the `docker-compose.yml` file and `Dockerfile`s.
The `docker-compose.yml` file is used to create a podman pod using `podman-compose` on the server.

## Services

### Nginx

Nginx acts as are reverse proxy for other services and serves them on a single port.
Note that the nginx config in this repository does not match the configuration running on the server.
This is due to the fact that production and development configuration still need to be separated (see https://github.com/mapsential/mapsential/issues/7#issue-1034484962).

### Frontend

url: http://mapsential.de <br/>

Frontend written in react with TypeScript.

### REST-API

url: http://mapsential.de/api <br/>

REST-API using the Spring Boot Java framework.

### Swagger UI

url: http://mapsential.de/api-docs <br/>

OpenAPI documentation for the REST-API endpoints, rendered using Swagger UI.

### Admin Backend

Backend for populating the database. Uses piccolo-orm and piccolo admin. The url for the admin-site is http://mapsential.de/piccolo-admin.

### Database

PostgreSQL Database.


## Installation

1. Make sure you are running linux or a linux vm.
2. Install `podman` https://podman.io/getting-started/installation.html
3. Install `podman-compose`  https://github.com/containers/podman-compose
4. Install `pass` https://www.passwordstore.org/
5. Ask maintainers for gpg private and public keys or rewrite the contents of `encrypted-secrets` with your own pass store
6. If you are using the gpg keys from the maintainers then import them using `gpg --import <pub_key>.gpg` and `gpg --allow-secret-key-import --import <secret_key>.gpg`
7. Clone the repo
8. Run `source setup_pass.sh` in the repo's root directory
9. Run `create_podman_secrets.sh` in the repo's root directory
10. Run `podman-compose up` in the repo's root directory and select where to download the base images when prompted

After this completes you should see the website running at `127.0.0.1:8000`

# Deployment

> **Important:** If you are running rootless podman in an ssh session the run [`loginctl enable-linger`](https://github.com/containers/podman/blob/main/troubleshooting.md#21-a-rootless-container-running-in-detached-mode-is-closed-at-logout).
