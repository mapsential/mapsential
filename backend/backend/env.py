import os
from typing import Literal


def is_production() -> bool:
    return is_environment("prod")


def is_docker_dev() -> bool:
    return is_environment("docker-dev")


def is_environment(expected_environment: Literal["prod", "docker-dev"]) -> bool:
    return os.environ["ENV"] == expected_environment
