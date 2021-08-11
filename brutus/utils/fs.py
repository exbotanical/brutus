"""
This module contains utilities for file-system operations
"""
from os import path
from typing import Generator, Union

ROOT_DIR = path.dirname(path.dirname(__file__))
ROOT_DIR_ABS = path.realpath(ROOT_DIR)


class FileChunk:
    """
    FileChunk represents a single, iterable chunk of memory read
    from a file descriptor
    """

    def __init__(self, filename, start, end):
        self.__filename = filename
        self.__fp = None
        self.__start = start
        self.__end = end

    def __iter__(self):
        while self.__fp.tell() < self.__end:
            yield self.__fp.readline()

    def __enter__(self):
        return self

    def __exit__(self, ex_type, ex_val, traceback):
        # remember, we need to have these 3 ^ in the function signature,
        # as this builtin will be called with them
        self.close()
        return True

    def open(self, mode: str = 'r') -> 'FileChunk':
        """Opens a file descriptor at the `start` offset

        Args:
            mode (str, optional): Read mode. Defaults to 'r'.

        Returns:
            FileChunk: instance itself so methods may be chained
        """
        try:
            self.__fp = open(self.__filename, mode)
        except (OSError, IOError):
            pass  # TODO logging

        self.__fp.seek(self.__start)
        return self

    def close(self) -> None:
        """Closes the FileChunk descriptor"""
        self.__fp.close()

    def seek(self, pos: int) -> None:
        """Seek the FileChunk descriptor's cursor to the provided offset `pos`

        Args:
            pos (int): Position to seek to; must be greater than FileChunk start,
            less than FileChunk end
        """
        if pos < self.__start or pos > self.__end:
            pass  # TODO logging

        self.__fp.seek(pos)

    def read(self) -> Union[bytes, str]:
        """Read the FileChunk into memory

        Returns:
            Union[bytes, str]: File contents
        """
        return self.__fp.read(self.__end - self.__fp.tell())


def resolve_rootdir(*fpaths: str) -> str:
    """Resolve an absolute path of `fpaths` from the Brutus root directory\n
    NOTE: The returned path is not guaranteed to exist

    Args:
        *fpaths (tuple): the paths on which to resolve

    Returns:
        str: an absolute path from the Brutus root directory to the provided
            path concatenation
    """
    return path.join(ROOT_DIR_ABS, *fpaths)


def resolve_scriptsdir(filename: str) -> str:
    """Resolve the provided path on the Brutus scripts directory\n
    NOTE: The returned path is not guaranteed to exist

    Args:
        filename (str): The path to resolve from the scripts directory;
            typically a single filename

    Returns:
        str: An absolute path to the specified `filename` in the
        Brutus scripts directory
    """
    return resolve_rootdir('scripts', filename)


def split_file(abs_filename: str, n_chunks: int) -> Generator:
    """Split a file into N chunks by seeking and moving a file pointer.
    Important to note about this method is it is optimized for speed
    and not precision.

    When we seek, we move the file pointer K bytes forward, then read to the end of
    whatever line we've landed in.

    This method is for parsing wordlists and very large files where we may wish to have
    multi-processing or multi-threading in place to handle the resulting chunks.

    Args:
        abs_filename (str): Absolute file path. Caller is responsible for
        ensuring it exists
        n_chunks (int): Number of chunks to break the file into

    Yields:
        list: A list of file readers set at varying cursor positions
    """
    size = path.getsize(abs_filename)
    chunk_size = size // n_chunks

    fp = open(abs_filename, 'rb')

    # seek in the file chunk_size bytes, then read a line to get a line ending
    pos = 0
    eof = False

    while not eof:
        prev_pos = pos
        fp.seek(chunk_size, 1)

        if not fp.readline():
            fp.seek(0, 2)
            eof = True

        pos = fp.tell()

        yield FileChunk(abs_filename, prev_pos, pos)

    fp.close()
