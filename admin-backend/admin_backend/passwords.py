import subprocess
from pathlib import Path

import env
from paths import PROJECT_DIR


def get_password(password_path: str) -> str:
    if (secret_path := Path(f"/run/secrets/{password_path.replace('/', '_')}")).exists():
        with open(secret_path) as f:
            return f.read()

    func = get_docker_dev_password if env.is_docker_dev() else get_prod_password

    return func(password_path)


def get_prod_password(password_path: str) -> str:
    return subprocess.run([
        "bash", "-c", f"source {PROJECT_DIR}/setup_pass.sh && pass {password_path}"
    ], capture_output=True).stdout.decode("utf-8").strip()


def get_docker_dev_password(password_path: str) -> str:
    with open(PROJECT_DIR / "docker_dev_plaintext_secrets" / f"{password_path}.txt") as f:
        return f.read()
