import subprocess

from os import path

from .fs import resolve_scriptsdir
from .errors.shell_err import ScriptFailed

def invoke_script(
    script: str,
    args: str = None,
    throw_on_fail: bool = True,
    autoresolve = True
) -> int:

    if autoresolve:
        script_path = resolve_scriptsdir(script)
    else:
        script_path = script

    if not path.exists(script_path):
        raise FileNotFoundError

    proc = subprocess.Popen(['bash', script_path, args])
    proc.wait()
    (stdout, stderr) = proc.communicate()

    if proc.returncode != 0 and throw_on_fail:
        raise ScriptFailed(stderr=stderr, returncode=proc.returncode)
