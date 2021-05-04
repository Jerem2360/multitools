from multi_tools.stdio import text_io
from multi_tools.console.colors import AnsiColor
from multi_tools.console import colors, io_counters
import sys
import time

class OStream(text_io.TextIO):

    def __init__(self, __color_fg: AnsiColor = None):
        self.ansi_color_fg = ""
        self.ansi_color_fg_reset = ""
        text_io.TextIO.__init__(self, sys.stdout, customName=f"ConsoleOStream-{io_counters.Ostream_counter.value}")
        io_counters.Ostream_counter.incr()
        if colors.Ansi.enabled:
            if __color_fg is not None:
                self.ansi_color_fg = f"\033[{__color_fg.id}m"
                self.ansi_color_fg_reset = "\033[39m"

    def apply_ansi(self, code: colors.CustomAnsiObject):
        self.write(f"\033[{code.code}m")

    def __write__(self, text: str):
        """
        Implement color config for self.write()
        """
        super().__write__(self.ansi_color_fg + text + self.ansi_color_fg_reset)


class IStream(text_io.TextIO):

    def __init__(self):
        text_io.TextIO.__init__(self, sys.stdin, customName=f"ConsoleIStream-{io_counters.Istream_counter.value}")
        io_counters.Istream_counter.incr()

    def __read__(self, size: int, spec=False):
        """
        Implement self.read()
        """
        super().__read__(size, spec=True)


