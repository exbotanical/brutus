from os import path

ROOT_DIR = path.dirname(path.dirname(__file__))
ROOT_DIR_ABS = path.realpath(ROOT_DIR)

def resolve_rootdir(*paths: tuple) -> str:
  return path.join(ROOT_DIR_ABS, *paths)

def resolve_scriptsdir(path: str) -> str:
	return resolve_rootdir('scripts', path) # TODO use a constant
