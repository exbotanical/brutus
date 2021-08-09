from os import path, unlink

FIXTURES = path.abspath(path.join(path.dirname(__file__), 'fixtures'))


def resolve_fixture(p: str) -> str:
    """Retrieve the path to a given fixture

    Args:
        p (str): the fixture name (filename)

    Returns:
        str: full path to fixture
    """
    return path.join(FIXTURES, p)


def compare_lines(filename: str, basename: str, n: int) -> bool:
    """Compare a source file's lines with those of N separate files' lines
    in ordered sequence. This is helpful for `split_file`, where we split a file into
    chunks.

    Args:
        filename (str)
        basename (str)
        n (int)

    Returns:
        bool
    """
    with open(filename, 'r') as src:
        for i in range(n):
            with open(basename + '{:02}'.format(i), 'r') as dest:
                for line in dest:
                    if line != src.readline():
                        return False
    return True


def remove_files(filenames: list, n: int) -> None:
    """Remove files

    Args:
        filenames (str)
        n (int)
    """
    for basename in filenames:
        for i in range(n):
            unlink(basename + '{:02}'.format(i))
