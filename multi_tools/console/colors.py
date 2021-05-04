from typing import Union, Literal, final


@final
class _Ansi:
    def __init__(self):
        self.enabled = False

    def enable_ansi(self):
        self.enabled = True
        import ctypes
        kernel32 = ctypes.WinDLL('kernel32')
        hStdOut = kernel32.GetStdHandle(-11)
        mode = ctypes.c_ulong()
        kernel32.GetConsoleMode(hStdOut, ctypes.byref(mode))
        mode.value |= 4
        kernel32.SetConsoleMode(hStdOut, mode)


Ansi = _Ansi()


class AnsiColor:
    def __init__(self, code: Union[Literal[30], Literal[31], Literal[32], Literal[33], Literal[34], Literal[35],
                                   Literal[36],  Literal[37]]):
        self.id = code

    def __repr__(self):
        return f"<AnsiConsoleColor at {id(self)}, code={self.id}>"


class CustomAnsiObject:
    def __init__(self, code: int):
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
            self.type = "Unknown"

    def __repr__(self):
        return f"<AnsiConsoleObject at {id(self)}, code={self.code}, type={self.type}>"


BLACK = AnsiColor(30)
RED = AnsiColor(31)
GREEN = AnsiColor(32)
YELLOW = AnsiColor(33)
BLUE = AnsiColor(34)
MAGENTA = AnsiColor(35)
CYAN = AnsiColor(36)
WHITE = AnsiColor(37)
