from multi_tools.console import io
import sys


class AnsiAction:
    def __init__(self, ostream: io.OStream = None):
        """
        Pretty much the same objective than for colors.AnsiColor,
        but for ansi codes that act on the console screen layout.
        Acts only on the specified ostream, so it can be used independantly
        on each ostream of your program. This feature isn't fully implemented
        yet.
        Takes one optional parameter, 'ostream' which is a console.io.OStream
        object and defaults to sys.stdout.
        """
        self.ostream = ostream

    def set_title(self, title: str):
        """
        Set the title of the current console window, using ansi codes
        """
        action = f"\033]2;{title}\a"
        self.__exec__(action)

    def clear_screen(self, mode=2):
        """
        Clear the console from any text.
        """
        action = f"\033[{mode}J"
        self.__exec__(action)

    def clear_line(self, mode=2):
        """
        Same as clear(), but clear only the last line
        of the console.
        """
        action = f"\033[{mode}K"
        self.__exec__(action)

    def cursor_up(self, amount=1):
        """
        Move the cursor up by amount.
        """
        action = f"\033[{amount}A"
        self.__exec__(action)

    def cursor_down(self, amount=1):
        """
        Move the cursor down by amount.
        """
        action = f"\033[{amount}B"
        self.__exec__(action)

    def cursor_right(self, amount=1):
        """
        Move the cursor right by amount.
        """
        action = f"\033[{amount}C"
        self.__exec__(action)

    def cursor_left(self, amount=1):
        """
        Move the cursor left by amount.
        """
        action = f"\033[{amount}D"
        self.__exec__(action)

    def __exec__(self, action: str):
        """
        Execute the demanded action (ansi code) on the demanded ostream.
        Only for internal use.
        """
        if self.ostream is None:
            sys.stdout.write(action)
        else:
            self.ostream.write(action)
