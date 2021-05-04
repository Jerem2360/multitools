from multi_tools.stdio import text_io
from multi_tools.console.colors import AnsiColor
from multi_tools.console import colors, io_counters
import sys

class OStream(text_io.TextIO):

    def __init__(self, __color_fg: AnsiColor = None):
        """
        A type that represents a console stream that
        can write to the console, but has it's own text foreground
        color that doesn't act on the other streams' fg colors.
        This way, you can easily write in different color to the
        console without bothering about ansi.
        Takes one optional argument '__color_fg' defining the foreground
        color of the text it will print to the console.
        """
        self.ansi_color_fg = ""
        self.ansi_color_fg_reset = ""
        text_io.TextIO.__init__(self, sys.stdout, customName=f"ConsoleOStream-{io_counters.Ostream_counter.value}")
        io_counters.Ostream_counter.incr()
        if colors.Ansi.enabled:
            if __color_fg is not None:
                self.ansi_color_fg = f"\033[{__color_fg.id}m"
                self.ansi_color_fg_reset = "\033[39m"

    def apply_ansi(self, code: colors.CustomAnsiObject):
        """
        Apply a CustomAnsiObject to the console.
        """
        self.write(f"\033[{code.code}m")

    def __write__(self, text: str):
        """
        Implement color config for self.write()
        """
        super().__write__(self.ansi_color_fg + text + self.ansi_color_fg_reset)


class IStream(text_io.TextIO):

    def __init__(self):
        """
        A type that represents a console stream that can only read from the
        console. Useful for organizing the different reasons to read from
        the console in your project.
        """
        text_io.TextIO.__init__(self, sys.stdin, customName=f"ConsoleIStream-{io_counters.Istream_counter.value}")
        io_counters.Istream_counter.incr()

    def __read__(self, size: int, spec=False):
        """
        Implement self.read()
        """
        super().__read__(size, spec=True)


