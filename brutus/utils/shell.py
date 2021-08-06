import subprocess

from os import path

from .fs import resolve_scriptsdir
from .errors.shell_err import ScriptFailed

def invoke_script(
    script: str,
    args: str = None,
    throw_on_fail: bool = True,
    autoresolve = True
) -> None:
    """Invoke a shell script

    Args:
        script (str): the shell script name
        args (str, optional): arguments to pass on to the script; Defaults to None.
        throw_on_fail (bool, optional): raise a `ScriptFailed` exception on non-zero return codes? Defaults to True.
        autoresolve (bool, optional): resolve the script path relative to the Brutus scripts directory? Defaults to True.

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
