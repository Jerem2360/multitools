from multi_tools.console import io
from multi_tools.console.colors import BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
from multi_tools.console import colors, control
import sys

OStream = io.OStream  # A type that represents output (write) streams.

IStream = io.IStream  # A type that represents input (read) streams.

Action = control.AnsiAction  # A type that represents the graphical configs of the console.

def configure():
    """
    Activate ansi codes for the command prompt.
    **Only works on Windows!**
    """
    colors.Ansi.enable_ansi()


print = io.print_

