"""
Brutus is an educational exploitation kit
"""
from .interfaces.web_crawler.inquirer import run
from .utils.logger import LOGGER

try:
    LOGGER.info('init')
    run()
except KeyboardInterrupt:
    LOGGER.info('cancelled')
