#!/bin/bash

set -e

cd "$( dirname "${BASH_SOURCE[0]}" )" || exit 1

function repopulate_database() {
    admin_backend_cmd="
        cd admin_backend && 
        echo 'Running database migrations...' && 
        piccolo forward all && 
        echo 'Adding defibrillators to database...' && 
        python data_acquisition/defibrillators.py && 
        echo 'Adding drinking fountains to database...' && 
        python data_acquisition/drinking_fountains.py && 
        echo 'Adding soup kitchens to database...' && 
        python data_acquisition/soup_kitchens.py && 
        echo 'Adding toilets to database...' && 
        python data_acquisition/toilets.py
    "

    docker exec -it mapsential_admin_backend bash -c "${admin_backend_cmd}"
}

if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    repopulate_database
fi
