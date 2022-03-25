#!/bin/bash

project_dir=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source "${project_dir}/setup_pass.sh"

# Remove current secrets
podman secret rm -a

pass postgres/password | podman secret create postgres_password -

pass email/clemens | podman secret create email_clemens -
pass email/denis | podman secret create email_denis -
pass email/lucas | podman secret create email_lucas -
pass email/orhun | podman secret create email_orhun -
pass email/oscar | podman secret create email_oscar -

pass piccolo_admin_password/clemens | podman secret create piccolo_admin_password_clemens -
pass piccolo_admin_password/denis | podman secret create piccolo_admin_password_denis -
pass piccolo_admin_password/lucas | podman secret create piccolo_admin_password_lucas -
pass piccolo_admin_password/orhun | podman secret create piccolo_admin_password_orhun -
pass piccolo_admin_password/oscar | podman secret create piccolo_admin_password_oscar -

unset project_dir
