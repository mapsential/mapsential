#!/bin/bash

# Get a postgres psql shell on the database container.

container_name=$( podman ps | grep 'mapsential_db' | awk '{print $1}' )

# Switch to the postgres user and run `psql` using a bash shell running
# as an interactive tty on the project's postgres container.
podman exec -it "$container_name" /bin/bash -c 'su -c "psql" postgres'

unset container_name
