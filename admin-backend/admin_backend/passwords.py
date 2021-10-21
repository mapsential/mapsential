import subprocess

from paths import PROJECT_DIR


def get_password(password_path: str) -> str:
    return subprocess.run([
        "bash", "-c", f"source {PROJECT_DIR}/setup_pass.sh && pass {password_path}"
    ], capture_output=True).stdout.decode("utf-8").strip()
