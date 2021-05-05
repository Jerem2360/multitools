from multi_tools.errors import exceptions
import traceback
import sys


IOError_ = exceptions.IOError_

ErrorImitation = exceptions.ErrorImitation

raise_ = exceptions.raise_


def format_exc(type_, value, tb):
    result = ""
    for text in traceback.TracebackException(*sys.exc_info()).format(chain=True):
        result += text

    return result
