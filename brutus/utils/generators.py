"""
This module contains generator utilities
"""
import random


def generate_n_ints(num: int = 6) -> list:
    """Generate a list of `num` pseudo-random integers

    Args:
        num (int, optional): N integers to generate. Defaults to 6.

    Returns:
        list: list of pseudo-random integers
    """
    return [random.randrange(256) for _ in range(num)]
