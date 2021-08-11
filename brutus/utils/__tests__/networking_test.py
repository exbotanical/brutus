import unittest

from ..networking import hostname_resolves, ipaddr_valid


class TestNetworkingUtils(unittest.TestCase):
    """
    Test networking utilities
    """

    def test_hostname_resolves(self):
        self.assertTrue(hostname_resolves('google.com'))
        self.assertFalse(hostname_resolves('0ss'))

    def test_ipaddr_valid(self):
        self.assertTrue(ipaddr_valid('127.0.0.1'))
        self.assertFalse(ipaddr_valid('0'))


if __name__ == '__main__':
    unittest.main()
