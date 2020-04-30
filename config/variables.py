import os

ENCODING_REGEX = "Accept-Encoding:.*?\\r\\n"
LEN_REGEX = "(?:Content-Length:\s)(\d*)"
INJECTION_REGEX = "</body>"
WINDOWS_PYTHON_INTERPRETER_PATH = os.path.expanduser("~/.wine/drive_c/Python27/Scripts/pyinstaller.exe")
HREF_REGEX = '(?:href=")(.*?)"'
XSS_SIMULACRUM = "<sCript>alert('test')</scriPt>"
SQLI_SIMULACRA = ["'", "' or 1=1;--", "1\' or \'1\' = \'1\''", "' or 1=1--","' or 1=1#","' or 1=1/*","') or '1'='1--", "') or ('1'='1--"]
DB_SQLI_SIMULACRA = ["'", "')", "';", '"', '")', '";', '`', '`)', '`;', '\\', "%27", "%%2727", "%25%27", "%60", "%5C"]
