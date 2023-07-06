from os import getenv
from typing import Optional

from .all import Settings


def get_settings(env: Optional[str] = None) -> Settings:
    return Settings(_env_file=f"env/.{env}")


def _get_settings(env: Optional[str] = None) -> Settings:
    return get_settings(env)



settings = _get_settings(getenv("ENV", "development"))