"""This module exposes APIs for soliciting system information and metadata
"""
import getpass
import platform
from enum import Enum


class OperatingSystem(Enum):
    """Denotes an Operating System type"""

    LINUX = (1,)
    DARWIN = (2,)
    WINDOWS = (3,)
    UNKNOWN = -1


class SystemInfo:
    """Represents a keyed object for storing system information"""

    __slots__ = ('os', 'machine_name', 'user', 'arch', 'processor')

    def __init__(self, os, mach_name, user, arch, proc) -> None:
        self.os = os
        self.machine_name = mach_name
        self.user = user
        self.arch = arch
        self.processor = proc


def get_sysinfo() -> SystemInfo:
    """Get base information for a system

    Returns:
        SystemInfo
    """
    uname = platform.uname()

    info = SystemInfo(
        os=uname[0] + ' ' + uname[2] + ' ' + uname[3],
        mach_name=uname[1],
        user=getpass.getuser(),
        arch=uname[4],
        proc=uname[5],
    )

    return info


def get_os() -> OperatingSystem:
    """Get the operating system of the host machine

    Returns:
        OperatingSystem
    """
    os = platform.system()
    if os == 'Linux':
        return OperatingSystem.LINUX
    if os == 'Darwin':
        return OperatingSystem.DARWIN
    if os == 'Windows':
        return OperatingSystem.WINDOWS
    return OperatingSystem.UNKNOWN
