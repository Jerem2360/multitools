from multi_tools.console import io
import sys


class AnsiAction:
    def __init__(self, ostream: io.OStream = None):
        self.ostream = ostream

    def set_title(self, title: str):
        action = f"\033]2;{title}\a"
        self.__exec__(action)

    def clear_screen(self, mode=2):
        action = f"\033[{mode}J"
        self.__exec__(action)

    def clear_line(self, mode=2):
        action = f"\033[{mode}K"
        self.__exec__(action)

    def cursor_up(self, amount=1):
        action = f"\033[{amount}A"
        self.__exec__(action)

    def cursor_down(self, amount=1):
        action = f"\033[{amount}B"
        self.__exec__(action)

    def cursor_right(self, amount=1):
        action = f"\033[{amount}C"
        self.__exec__(action)

    def cursor_left(self, amount=1):
        action = f"\033[{amount}D"
        self.__exec__(action)

    def __exec__(self, action: str):
        if self.ostream is None:
            sys.stdout.write(action)
        else:
            self.ostream.write(action)
