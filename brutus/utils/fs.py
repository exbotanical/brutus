from os import path

ROOT_DIR = path.dirname(path.dirname(__file__))
ROOT_DIR_ABS = path.realpath(ROOT_DIR)


def resolve_rootdir(*fpaths: tuple) -> str:
    """Resolve an absolute path of `fpaths` from the Brutus root directory\n
    NOTE: The returned path is not guaranteed to exist

    Args:
        *fpaths (tuple): the paths on which to resolve

    Returns:
        str: an absolute path from the Brutus root directory to the provided path concatenation
    """
    return path.join(ROOT_DIR_ABS, *fpaths)


def resolve_scriptsdir(fpath: str) -> str:
    """Resolve the provided path on the Brutus scripts directory\n
    NOTE: The returned path is not guaranteed to exist

    Args:
        fpath (str): the path to resolve from the scripts directory; typically a single filename

    Returns:
        str: an absolute path to the specified `fpath` in the Brutus scripts directory
    """
    return resolve_rootdir('scripts', fpath)  # TODO use a constant
