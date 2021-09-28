#!/bin/bash

project_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

export PASSWORD_STORE_DIR="${project_dir}/encrypted_secrets"

unset project_dir
