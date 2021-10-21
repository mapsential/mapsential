import os


def is_production() -> bool:
    return os.getenv("IS_PROD", None) == "true"
