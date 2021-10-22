import os
import sys


"""
Dll managing to make sure that all dlls are present
and up-to-date. Uses AppData so that any file
can access them from absolute path without
bothering with relative paths.
"""


# List of dlls that need to be imported / updated for multi_tools:
dlls = ['pointer.dll', 'memory.dll']


if sys.platform != "win32":
    raise NotImplementedError(
        "multi_tools is not designed to work on other platforms "
        "than windows, support may be added later on."
    )


def _tryopen(file):
    if os.path.exists(file):
        return open(file, "rb+")
    return open(file, "xb+")


def _copyfile(source, destination):  # helper function for copying files.
    s = open(source, "rb+")
    contents = s.read()
    s.close()
    print(os.path.exists(destination))
    if os.path.exists(destination):
        with _tryopen(destination) as x:
            getdest = x.read()

        if getdest != contents:
            sys.stderr.write("Updating multitools file '{0}'".format(dest))
            dest_ = open(destination, "wb+")
            dest_.write(contents)
            dest_.close()
    else:
        with _tryopen(destination) as x:
            getdest = x.read()

        if getdest != contents:
            sys.stderr.write("Updating multitools file '{0}'".format(dest))
            dest_ = open(destination, "rb+")
            dest_.write(contents)
            dest_.close()


# constants that depend on the system:
APPDATA = os.getenv("AppData") + "\\.pyCpp\\"
DLLPATH = "multi_tools/dlls/"


# create our own AppData/Roaming/... subfolder if it doesn't already exist:
if not os.path.exists(APPDATA):
    os.mkdir(APPDATA)


# update listed dlls to their corresponding version:
for dll in dlls:
    src = DLLPATH + dll
    dest = APPDATA + dll
    if not os.path.exists(APPDATA):
        os.mkdir(APPDATA)
    _copyfile(src, dest)


"""
Importing functions from submodules:
"""

from multi_tools import file_io
from multi_tools import stdio
from multi_tools import console
from multi_tools import data
from multi_tools import arrays

# path-related functions:

openfile = file_io.file  # for a complete description, see multi_tools.file_io.file()
# usage:
# file = multi_tools.openfile("folder/example.txt")
# file.write("hello")
# x = file.read()

createfile = file_io.nfile  # for a complete description, see multi_tools.file_io.nfile()
# usage:
# multi_tools.createnewfile("folder/example2.txt")


# console-related objects:

stdout = stdio.stdout
stdin = stdio.stdin
stderr = stdio.stderr


def printf(text: str, end="\n", ostream: console.OStream = None):
    if ostream is None:
        sys.stdout.write(text + end)
    else:
        ostream.write(text, end=end)


abstractmethod = data.AbstractMethod


def format_id(obj):
    hex_ = hex(id(obj))
    return str(hex_).upper()


def typename(obj):
    return eval("type(obj).__name__", {'obj': obj, **globals()}, locals())


def string_inner(s: str, **extra):
    try:
        a = eval(s, {**extra, **globals()}, locals())
    except NameError:
        return ''

    return a

