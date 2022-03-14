#!/bin/bash

set -e

# Setup
# ============================================================================

original_dir="$( pwd )"
# cd to directory of script. Means script can be run from outside directory.
cd "$( dirname "${BASH_SOURCE[0]}" )" || exit

# Test
# ============================================================================

# Run pytest within pipenv virtual environment and pass command line arguments to pytest.
pipenv run python -m pytest "$@"


# Teardown
# ============================================================================

# Return to original directory from which the script was executed.
cd "$original_dir" || exit
unset "$original_dir"
