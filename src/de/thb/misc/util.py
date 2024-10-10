import logging.config
import yaml

LOG_CONFIG_PATH: str = '../../../../../../resources/util/logging_config.yaml'


def setup_logging() -> None:
    with open(LOG_CONFIG_PATH, 'r') as f:
        config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
