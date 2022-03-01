#!/bin/bash

set -e

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit 1

env=$1

if [[ $env == "docker-dev" ]]; then
    db_host="db"
    # TODO: Do not hardcode dev password here.
    # Password should have single source of truth
    db_password="dev-postgres-password"
else
    db_host="localhost"
    db_password="$(cat /run/secrets/postgres_password)"
fi

file_path="src/main/resources/application.properties"

sed -e "s/{{db_host}}/${db_host}/g" \
    -e "s/{{db_password}}/${db_password}/g" \
    "${file_path}.template" \
    > $file_path