"""
This module contains utilities for shell operations
"""
import subprocess
from os import path, system

from .exceptions import ScriptFailed
from .fs import resolve_scriptsdir
from .logger import LOGGER
from .sys import OperatingSystem, get_os


def invoke_script(
    script: str, args: str = '', throw_on_fail: bool = True, autoresolve: bool = True
) -> None:
    """Invoke a shell script

    Args:
        script (str): the shell script name
        args (str, optional): arguments to pass on to the script; Defaults to ''.
        throw_on_fail (bool, optional): raise a `ScriptFailed` exception on non-zero
            return codes? Defaults to True.
        autoresolve (bool, optional): resolve the script path relative to the Brutus
            scripts directory? Defaults to True.

    Raises:
        FileNotFoundError: `script` path does not exist
        ScriptFailed: script results in a non-zero return code
    """
    if autoresolve:
        script_path = resolve_scriptsdir(script)
    else:
        script_path = script

    if not path.exists(script_path):
        raise FileNotFoundError

    proc = subprocess.Popen(['bash', script_path, args])
    proc.wait()
    (_, stderr) = proc.communicate()

    if proc.returncode != 0 and throw_on_fail:
        raise ScriptFailed(stderr=stderr, returncode=proc.returncode)


def spawn_new_shell(pkg: str) -> None:
    """Launch a new terminal emulator (shell)
    For starters, our defaults are gnome-terminal (linux) and Terminal (macos)

    Someone will need to open a PR for Windows support as
    I have no clue about their software.

    Args:
        pkg (str): the exact Brutus module path of the module we want to
        invoke in the new shell
    """
    _os = get_os()
    dir_path = path.dirname(path.dirname(__file__))

    if _os == OperatingSystem.LINUX:
        system(
            f'gnome-terminal -e 2>/dev/null \'bash -c \"python3 -m {pkg}; exec bash\"\''
        )
    elif _os == OperatingSystem.DARWIN:
        system(
            f'''osascript -e 'tell app 'Terminal'
        do script 'cd {dir_path}; python3 -m {pkg}'
        end tell' '''
        )
    elif _os == OperatingSystem.WINDOWS:
        LOGGER.info(
            'this package does not currently support Windows. Have a fix? Submit a PR!'
        )
    else:
        LOGGER.warn('Your operating system does not support this package.\n')


def attempt_script(scriptname: str) -> bool:
    """Attempt to execute a script; handles errors

    Args:
        scriptname (str)

    Returns:
        bool: Was the result of calling the script in any way erroneous?
    """
    try:
        invoke_script(scriptname)

        return True

    except ScriptFailed as sf_ex:
        LOGGER.error(sf_ex.message)

        return False

    except Exception:  # pylint: disable=W0703
        LOGGER.fatal(
            'something went wrong; please file an issue on the author\'s GitHub'
        )

        return False
