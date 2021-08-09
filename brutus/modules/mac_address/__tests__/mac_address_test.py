import re
import unittest

from ..MacAddressManager import MACADDR_REGEX, MacAddressManager


class TestMacAddressManager(unittest.TestCase):
    """
    Test MAC address utilities
    """

    def test_generate_macaddr_random(self):
        self.assertIsNotNone(
            re.search(MACADDR_REGEX, MacAddressManager.generate_macaddr())
        )

    def test_generate_macaddr_oui(self):
        self.assertIsNotNone(
            re.search(
                'aa:bb:cc:[0-9a-f]{2}(:)[0-9a-f]{2}',
                MacAddressManager.generate_macaddr(oui='aa:bb:cc'),
            )
        )

    def test_validate_macaddr_format(self):
        self.assertFalse(MacAddressManager.validate_macaddr_format('aa:bb:cc:dd:gg:zz'))
        self.assertFalse(MacAddressManager.validate_macaddr_format('11:22:33:44:55:vv'))
        self.assertFalse(MacAddressManager.validate_macaddr_format('12-33-54-aa-cc-aa'))
        self.assertFalse(
            MacAddressManager.validate_macaddr_format('11:22:33:44:55:66:11')
        )

        self.assertTrue(MacAddressManager.validate_macaddr_format('aa:bb:cc:dd:ee:ff'))
        self.assertTrue(MacAddressManager.validate_macaddr_format('11:22:33:44:55:66'))
        self.assertTrue(MacAddressManager.validate_macaddr_format('aa:11:3d:a7:00:dd'))

    def test_validate_oui_format(self):
        self.assertFalse(MacAddressManager.validate_oui_format('aa:bb:cc:aa'))
        self.assertFalse(MacAddressManager.validate_oui_format('11:22:33:33:33:33'))
        self.assertFalse(MacAddressManager.validate_oui_format('12-33-54'))

        self.assertTrue(MacAddressManager.validate_oui_format('aa:bb:cc'))
        self.assertTrue(MacAddressManager.validate_oui_format('11:22:33'))
        self.assertTrue(MacAddressManager.validate_oui_format('aa:11:3d'))


if __name__ == '__main__':
    unittest.main()
