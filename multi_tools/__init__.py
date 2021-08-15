from multi_tools import file_io
from multi_tools import stdio
from multi_tools import console
from multi_tools import data
import sys


# path-related functions:

openfile = file_io.file  # for a complete description, see multi_tools.file_io.file()
# usage:
# file = multi_tools.openfile("folder/example.txt")
# file.write("hello")
# x = file.read()

createnewfile = file_io.nfile  # for a complete description, see multi_tools.file_io.nfile()
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

