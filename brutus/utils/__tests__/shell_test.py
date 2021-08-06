import unittest
from os import path

from ..shell import invoke_script
from ..errors.shell_err import ScriptFailed

FIXTURES = path.abspath(path.join(
    path.dirname(__file__), 'fixtures'))

def fixture(p: str) -> str:
    return path.join(FIXTURES, p)

class TestShellUtils(unittest.TestCase):

    def test_invoke_script_nonexistent_file(self):
        with self.assertRaises(FileNotFoundError):
            invoke_script('noexist')

    def test_invoke_script_shellfail(self):
        with self.assertRaises(ScriptFailed):
            invoke_script(script=fixture('exit_with.bash'), args='1', autoresolve=False)


if __name__ == '__main__':
    unittest.main()
