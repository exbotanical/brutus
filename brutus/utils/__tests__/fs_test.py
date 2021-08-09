import unittest

from ..fs import split_file
from .utils import compare_lines, remove_files, resolve_fixture


class TestSplitFileUtil(unittest.TestCase):
    def setUp(self):
        self.src = resolve_fixture('wordlist.txt')
        self.artifacts = []
        self.n_chunks = 10
        self.descriptors = split_file(self.src, self.n_chunks)

    def tearDown(self):
        try:
            remove_files(self.artifacts, self.n_chunks)
        except (OSError, IOError):
            pass

    def test_split_file_iteration(self):
        basename = 'iterate'
        self.artifacts.append(basename)

        for i, fd in enumerate(self.descriptors):
            with fd.open('rb') as src, open(basename + '{:02}'.format(i), 'wb') as dest:
                for line in src:
                    dest.write(line)

        self.assertTrue(compare_lines(self.src, basename, self.n_chunks))

    def test_split_file_read(self):
        basename = 'read'
        self.artifacts.append(basename)

        for i, fd in enumerate(self.descriptors):
            with fd.open() as src, open(basename + '{:02}'.format(i), 'wb') as dest:
                dest.write(src.read())

        self.assertTrue(compare_lines(self.src, basename, self.n_chunks))


if __name__ == '__main__':
    unittest.main()
