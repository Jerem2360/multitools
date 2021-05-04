from typing import Union, Literal, final
import sys


@final
class _Ansi:
    def __init__(self):
        self.enabled = False

    def enable_ansi(self):
        """
        Enable ansi codes for the command prompt (the console).
        **Only works on Windows**
        """
        if sys.platform == "win32":
            self.enabled = True
            import ctypes
            kernel32 = ctypes.WinDLL('kernel32')
            hStdOut = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
            mode.value |= 4
            kernel32.SetConsoleMode(hStdOut, mode)
        else:
            raise NotImplementedError("This function is only implemented on Windows!")


Ansi = _Ansi()  # No explanations needed


class AnsiColor:
    def __init__(self, code: Union[Literal[30], Literal[31], Literal[32], Literal[33], Literal[34], Literal[35],
                                   Literal[36],  Literal[37]]):
        """
        A type representing a color in ansi code.
        It takes one parameter 'code' that should be one of the colors
        given as constants in this file.
        """
        self.id = code

    def __repr__(self):
        return f"<AnsiConsoleColor at {id(self)}, code={self.id}>"


class CustomAnsiObject:
    def __init__(self, code: int):
        """
        This type, is used to implement ansi actions that may
        not be implemented in this module.
        It takes one argument 'code', that needs to be a valid id
        for ansi actions.
        """
        self.code = code

        if code == 0:
            self.type = "Style.reset"
        elif code == 1:
            self.type = "Style.bright"
        elif code == 2:
            self.type = "Style.dim"
        elif code == 22:
            self.type = "Style.normal"
        elif 30 <= code <= 37:
            self.type = "Fg.standardColor"
        elif code == 39:
            self.type = "Fg.reset"
        elif 40 <= code <= 47:
            self.type = "Bg.standardColor"
        elif 90 <= code <= 97:
            self.type = "Fg.uncommonColor"
        elif 100 <= code <= 107:
            self.type = "Bg.uncommonColor"
        else:
            self.type = "Custom"

    def __repr__(self):
        return f"<AnsiConsoleObject at {id(self)}, code={self.code}, type={self.type}>"


# 8 basic colors of ansi:
BLACK = AnsiColor(30)
RED = AnsiColor(31)
GREEN = AnsiColor(32)
YELLOW = AnsiColor(33)
BLUE = AnsiColor(34)
MAGENTA = AnsiColor(35)
CYAN = AnsiColor(36)
WHITE = AnsiColor(37)
