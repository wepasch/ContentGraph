import logging.config
import yaml

from pathlib import Path
from typing import Any

LOG_CONFIG_PATH: str = 'util/logging_config.yaml'

def setup_logging() -> None:
    with open(get_resource(LOG_CONFIG_PATH), 'r') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)


def get_resource_dir() -> Path:
    return Path(get_root_dir().joinpath('resources'))


def get_root_dir() -> Path:
    return Path(__file__).parent.parent.parent.parent


def get_resource(rel_path: str) -> Path:
    return get_resource_dir().joinpath(rel_path)


def copy_without(src: dict[str, Any], excluded: set[str]) -> dict[str, Any]:
    return {k: src[k] for k in src.keys() - excluded}
