import unittest

from ..generators import generate_n_ints


class TestGeneratorUtils(unittest.TestCase):
    """
    Test generator utilities
    """

    def test_generate_n_ints_len(self):
        for i in range(9):
            self.assertEqual(len(generate_n_ints(i)), i)


if __name__ == '__main__':
    unittest.main()
