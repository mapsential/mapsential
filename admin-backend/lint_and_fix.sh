#!/bin/bash

# Setup
# ============================================================================

original_dir=$( pwd )
# cd to directory of script. Means script can be run from outside directory.
cd "$( dirname "${BASH_SOURCE[0]}" )" || exit


# Lint and fix
# ============================================================================

# Run pre-commit git hooks in pipenv virtual environment without needing to run `git commit`.
pipenv run pre-commit run --all-files


# Teardown
# ============================================================================

# Return to original directory from which the script was executed.
cd "$original_dir" || exit
unset "$original_dir"
