"""
Brutus is an educational exploitation kit
"""
from .interfaces.main_program.main_program import run_main_ui

# from .interfaces.web_crawler.inquirer import run
from .utils.logger import LOGGER

try:
    LOGGER.info('init')
    run_main_ui()

except KeyboardInterrupt:
    LOGGER.info('cancelled')
