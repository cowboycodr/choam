"""
find_dependencies finds project dependencies
and adds them to Choam.tomls
"""

import importlib
import os
import sys
from pathlib import Path

import findimports
import toml

IGNORE_DEPS = [
    "abc",
    "aifc",
    "argparse",
    "array",
    "ast",
    "asynchat",
    "asyncio",
    "asyncore",
    "atexit",
    "audioop",
    "bdb",
    "binascii",
    "binhex",
    "bisect",
    "builtins",
    "calendar",
    "cgi",
    "cgitb",
    "chunk",
    "cmath",
    "cmd",
    "code",
    "codecs",
    "codeop",
    "colorsys",
    "compileall",
    "configparser",
    "contextlib",
    "contextvars",
    "copy",
    "copyreg",
    "cProfile",
    "crypt",
    "csv",
    "ctypes",
    "dataclasses",
    "datetime",
    "decimal",
    "difflib",
    "dis",
    "doctest",
    "email",
    "encodings",
    "ensurepip",
    "enum",
    "errno",
    "faulthandler",
    "fcntl",
    "filecmp",
    "fileinput",
    "fnmatch",
    "fractions",
    "ftplib",
    "functools",
    "gc",
    "getopt",
    "getpass",
    "gettext",
    "glob",
    "graphlib",
    "grp",
    "gzip",
    "hashlib",
    "heapq",
    "hmac",
    "html",
    "http",
    "imaplib",
    "imghdr",
    "imp",
    "inspect",
    "io",
    "ipaddress",
    "itertools",
    "json",
    "keyword",
    "linecache",
    "locale",
    "logging",
    "lzma",
    "mailbox",
    "mailcap",
    "marshal",
    "math",
    "mimetypes",
    "mmap",
    "modulefinder",
    "msilib",
    "msvcrt",
    "multiprocessing",
    "netrc",
    "nis",
    "nntplib",
    "numbers",
    "operator",
    "optparse",
    "os",
    "ossaudiodev",
    "pathlib",
    "pdb",
    "pickle",
    "pickletools",
    "pipes",
    "pkgutil",
    "platform",
    "plistlib",
    "poplib",
    "posix",
    "pprint",
    "profile",
    "pstats",
    "pty",
    "pwd",
    "pyclbr",
    "pydoc",
    "queue",
    "quopri",
    "random",
    "re",
    "readline",
    "reprlib",
    "resource",
    "rlcompleter",
    "runpy",
    "sched",
    "secrets",
    "select",
    "selectors",
    "shelve",
    "shlex",
    "shutil",
    "signal",
    "site",
    "smtpd",
    "smtplib",
    "sndhdr",
    "socket",
    "socketserver",
    "spwd",
    "ssl",
    "stat",
    "statistics",
    "string",
    "stringprep",
    "struct",
    "subprocess",
    "sunau",
    "symtable",
    "sys",
    "sysconfig",
    "syslog",
    "tabnanny",
    "tarfile",
    "telnetlib",
    "tempfile",
    "termios",
    "test",
    "textwrap",
    "threading",
    "time",
    "timeit",
    "tkinter",
    "token",
    "tokenize",
    "trace",
    "traceback",
    "tracemalloc",
    "tty",
    "turtle",
    "turtledemo",
    "types",
    "typing",
    "unicodedata",
    "uu",
    "uuid",
    "venv",
    "warnings",
    "wave",
    "weakref",
    "webbrowser",
    "winreg",
    "winsound",
    "wsgiref",
    "xdrlib",
    "xml",
    "xmlrpc",
    "zipapp",
    "zipfile",
    "zipimport",
    "zlib",
    "zoneinfo",
]

def _find_dependencies(project_path: Path, project_name):
    """
    Find all dependencies of a given project

    :project_path: path to project

    :project_name: name of the project // necesarry for
    `Choam` to know the exact location of the project
    all of the project files.
    """

    import_info = set()

    files = Path(Path(project_path / project_name).absolute()).rglob("*.py")

    for file_name in files:
        import_info.update(findimports.find_imports(str(file_name)))

    dependencies = set()

    for imp in import_info:
        # Simplfying output to just module name
        dependency = repr(imp).split("'")[1]

        if dependency.startswith(project_name):
            continue

        if dependency in sys.builtin_module_names:
            continue

        if dependency in IGNORE_DEPS:
            continue

        dependencies.add(repr(imp).split("'")[1].split(".")[0])

    return dependencies


def find_dependencies():
    """
    Syntactic sugar for `_find_dependencies()`

    Automatically specifies the arguments
    `_find_dependencies()` for `Choam`'s needs.
    """

    project_path = Path(os.getcwd()).absolute()
    with open(f"{os.getcwd()}/Choam.toml", "r", encoding="utf-8") as file:
        config = toml.loads(file.read())

        project_name = config["package"]["name"]
        ignored_deps = config["modules-ignore"]

    found_depedencies = _find_dependencies(project_path, project_name)
    dependencies = []

    for dep in found_depedencies:
        if not importlib.util.find_spec(dep):
            continue

        if dep.strip() in IGNORE_DEPS:
            continue

        dependencies.append(dep)

    return dependencies

if __name__ == "__main__":
    print(IGNORE_DEPS)
    print(find_dependencies())
