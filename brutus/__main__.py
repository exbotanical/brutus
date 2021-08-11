"""
Brutus is an educational exploitation kit
"""
from .interfaces.main_program.main_program import run_main_ui
from .utils.logger import LOGGER

try:
    LOGGER.info('WELCOME TO BRUTUS')
    run_main_ui()

except KeyboardInterrupt:
    LOGGER.info('user cancelled the process')

except Exception:  # pylint: disable=W0703
    LOGGER.error('something went wrong...')
