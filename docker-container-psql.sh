#!/bin/bash

# Switch to the postgres user and run `psql` using a bash shell running
# as an interactive tty on the project's postgres container.
docker exec -it mapsential_db /bin/bash -c 'su -c "psql" postgres'

unset container_name
