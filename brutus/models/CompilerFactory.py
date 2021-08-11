"""Exposes an API for compiling Python scripts into executable binaries
"""

import PyInstaller.__main__  # type: ignore


class CompilerFactory:
    """Implements pyinstaller compilation interfaces"""

    def __init__(self, filename: str) -> None:
        # the file we are writing the compiled binary to
        # presumes the caller has validated the path

        self.filename = filename

    def compile_for_posix(self, hidden_imports: list) -> None:
        """Compile the payload for POSIX-compliant systems i.e. not Windows

        Args:
            hidden_imports (list) hidden imports,if any
        """
        args = [
            self.filename,
            '--onefile',
            '--noconsole',
            '-p /home/goldmund/repositories/brutus/brutus',
        ]

        for hidden_import in hidden_imports:
            args.append(f'--hidden-import={hidden_import}')

        PyInstaller.__main__.run(args)

    def compile_for_windows(self, hidden_imports: list) -> None:
        """Compile the payload for Window systems

        Args:
            hidden_imports (list) hidden imports, if any
        """
        args = [
            self.filename,
            '--onefile',
            '--noconsole',
            '-p /home/goldmund/repositories/brutus/brutus',
        ]

        for hidden_import in hidden_imports:
            args.append(f'--hidden-import={hidden_import}')

        PyInstaller.__main__.run(args)

    def write_file_imports(self, lines: list) -> None:
        """Write import statements to file pre-compilation

        Args:
            lines (list): text blocks to be written on newlines,
            where the newline is appended by this method
        """
        with open(self.filename, 'w+') as fd:
            fd.write('#!/usr/bin/env python3\n')
            for line in lines:
                fd.write(line + '\n')
