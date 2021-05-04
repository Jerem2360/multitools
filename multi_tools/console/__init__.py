from multi_tools.console import io
from multi_tools.console.colors import BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE
from multi_tools.console import colors, control

OStream = io.OStream

IStream = io.IStream

Action = control.AnsiAction

def configure():
    colors.Ansi.enable_ansi()


