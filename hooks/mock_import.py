#!/usr/bin/env python3
import __builtin__
from types import ModuleType
"""
Simulate imports to enable running the app instance on systems
which may not support all features (e.g. netflifyqueue)
"""
class DummyModule(ModuleType):
    def __getattr__(self, key):
        return None
    __all__ = []   # support wildcard imports

def tryimport(name, globals={}, locals={}, fromlist=[], level=-1):
    try:
        return realimport(name, globals, locals, fromlist, level)
    except ImportError:
        return DummyModule(name)

realimport, __builtin__.__import__ = __builtin__.__import__, tryimport

import sys   # works as usual
import foo   # no error

from bar import baz     # also no error
from quux import *      # ditto