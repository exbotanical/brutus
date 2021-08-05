import subprocess

from os import path

from brutus.utils.fs import resolve_scriptsdir

def invoke_shell_script(script: str, args=None) -> int:
	script_path = resolve_scriptsdir(script)

	if not path.exists(script_path):
		return 1

	return subprocess.call(['bash', script_path, args])
