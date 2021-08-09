"""This module implements a base class for all Brutus modules
"""


class BaseBrutusModule:
    """The BaseBrutusModule base class carries metadata common to all modules"""

    def __init__(
        self, requires_mitm_state: bool = False, requires_same_network: bool = False
    ) -> None:

        # does the module require the user to be in a MITM state?
        self.requires_mitm_state = requires_mitm_state
        self.requires_same_network = requires_same_network
