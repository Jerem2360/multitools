from multi_tools import file_io
from multi_tools import stdio
from multi_tools import console
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
