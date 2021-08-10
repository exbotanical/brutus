"""
Brutus is an educational exploitation kit
"""
from .interfaces.compilers.keylogger.inquirer import run

try:
    run()
except KeyboardInterrupt:
    print('hi')
