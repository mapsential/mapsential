#!/bin/bash

set -e

cwd="$( dirname "${BASH_SOURCE[0]}" )"

cd "$cwd" || exit 1

function docker_dev_compose() {
    docker-compose -f docker-compose.base.yml -f docker-compose.docker-dev.yml "$@"
}

source ./repopulate-database.sh

first_arg=$1
rest_args="${@:2}"

if [ "$first_arg" = "up" ]; then
    docker_dev_compose up $rest_args
elif [ "$first_arg" = "down" ]; then
    docker_dev_compose down $rest_args
elif [ "$first_arg" = "build" ]; then
    docker_dev_compose build $rest_args
elif [ "$first_arg" = "init" ]; then
    if [ -d "./db/pgdata" ]; then
        echo "Found existing database that must be removed"
        sudo rm -rf "./db/pgdata"
    fi

    if [ "$(docker ps | grep mapsential)" != "" ]; then
        docker_dev_compose down
    fi

    docker_dev_compose build --no-cache

    docker_dev_compose up --detach $rest_args

    repopulate_database
else
    echo "Expected 'up', 'down', 'build' or 'init' as first argument!"
    exit 1
fi