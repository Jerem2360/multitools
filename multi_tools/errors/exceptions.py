import sys
import traceback
from typing import Type


class IOError_(OSError):

    def __init__(self, text):
        """
        IO error.
        """
        OSError.__init__(self, text)


class ErrorImitation(BaseException):
    def __init__(self, name="ErrorImitation", text="This may not be an error. It's only an imitation.", immediateRaise=True):
        """
        Imitate a builtin exception, but with more flexibility.

        Takes 2 optional arguments, as so:

        Traceback (most recent call last):

        ... (stack trace)

        <name>: <text>


        And one last argument 'immediateRaise' that should be set
        to True if the error is raised with "raise ErrorImitation".
        Else, it should be False.
        """
        try:
            raise Exception
        except:
            self.lines = []
            for line in traceback.TracebackException(*sys.exc_info()).format(chain=True):
                self.lines.append(line)

            self.lines[len(self.lines) - 1] = f"{name}: {text}\n"

            if immediateRaise:
                self.__raise__()

    def __raise__(self):
        for ln in self.lines:
            sys.stderr.write(ln)

        sys.exit(1)


def raise_(error: Type[ErrorImitation], name, text):
    """
    Used to raise an ErrorImitation with more flexibility.
    """
    error.__raise__(error(name, text))
