import json
import logging
from pathlib import Path

from src.de.thb.misc.util import setup_logging

logger = logging.getLogger(__name__)

BASE_GRAPH_PATH: Path = Path("D:\\WS_Python\\Projects\\Content_Graph\\resources\\graphs\\base.json")

def main() -> None:
    with open(BASE_GRAPH_PATH, "r") as file:
        json_data: dict = json.load(file)
    if  json_data:
        logger.error(f'Failed to load data from {str(BASE_GRAPH_PATH)}')
        exit(1)


if __name__ == '__main__':
    setup_logging()
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    exit(9)
    main()
