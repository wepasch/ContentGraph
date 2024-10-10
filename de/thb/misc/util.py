import logging.config
import yaml


def setup_logging() -> None:
    with open('logging_config.yaml', 'rt') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)