import sys
import traceback
from typing import Type


class IOError_(OSError):
    def __init__(self, text):
        OSError.__init__(self, text)


class ErrorImitation(BaseException):
    def __init__(self, name="ErrorImitation", text="This may not be an error. It's only an imitation.", immediateRaise=True):
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
    error.__raise__(error(name, text))
