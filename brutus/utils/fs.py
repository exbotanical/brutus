from os import path

ROOT_DIR = path.dirname(path.dirname(__file__))
ROOT_DIR_ABS = path.realpath(ROOT_DIR)


def resolve_rootdir(*fpaths: tuple) -> str:
    return path.join(ROOT_DIR_ABS, *fpaths)


def resolve_scriptsdir(fpath: str) -> str:
    return resolve_rootdir('scripts', fpath)  # TODO use a constant
