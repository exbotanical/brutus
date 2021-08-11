"""
This module contains general utilities for use with Inquirer interfaces
"""
from typing import Callable


def destructure(answers: dict, *keys: str) -> list:
    """[summary]

    Args:
        answers (dict)

    Returns:
        list: an ordered list of values corresponding to the provided keys
    """
    return [answers[key] if key in answers else None for key in keys]


def validate(validator: Callable) -> Callable:
    """A wrapper for Inquirer validator functions;
    ensures we pass the answer to the validator and not the entire answers list

    Args:
        validator (Callable): actual validator function

    Returns:
        Callable: actual validator functions with a modified signature
    """

    def fn(_: dict, answer: str) -> bool:
        return validator(answer)

    return fn
