from multi_tools.errors import fexception
import traceback
import sys


def raise_f(err: fexception.FException):
    err.__raise__()

class FDefaultError:
    def __init__(self, text):
        self.text = text

    def __raise__(self):

        traceback.print_exc(file=sys.stderr)
