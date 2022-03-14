#!/bin/bash

set -e

original_dir="$( pwd )"
# cd to directory of script. Means script can be run from outside directory.
cd "$( dirname "${BASH_SOURCE[0]}" )" || exit

pipenv run vulture .

cd "$original_dir"
unset "$original_dir"