import subprocess
import sys
from typing import Literal


ContainerOrchestrator = Literal["podman", "docker"]


CONTAINER_ORCHESTATORS: list[ContainerOrchestrator] = ["podman", "docker"]


def run_command_in_container(
    orchestrator: ContainerOrchestrator,
    container_name: str,
    cmd: str
) -> int:
    return run_command_in_shell(f"{orchestrator} exec -it {container_name} /bin/bash -c '{cmd}'")


def is_running_container(
    orchestrator: ContainerOrchestrator,
    container_name: str
) -> bool:
    p1 = subprocess.Popen([orchestrator, "ps"], stdout=subprocess.PIPE)
    result = subprocess.run(
        ["grep", container_name],
        stdin=p1.stdout,
        capture_output=True
    )
    if p1.stdout is not None:
        p1.stdout.close()

    if result.returncode != 0:
        return False

    return container_name in result.stdout.decode()


def run_command_in_shell(cmd: str) -> int:
    """**Important:** Never use with user generated content!"""

    return subprocess.run(
        cmd,
        stdout=sys.stdout,
        stderr=sys.stderr,
        shell=True,
    ).returncode
