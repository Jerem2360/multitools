from multi_tools.system import registry
import sys
from typing import Literal


if sys.platform != 'win32':
    raise NotImplementedError("Module is only implemented on windows.")


_EventType = ["background", "file", "directory"]


class _BackgroundContextMenuType:
    def __init__(self):
        self.reg_path = [registry.Registry.HKEY_CLASSES_ROOT, "directory", "background", "shell"]

    def add_button(self, name: str, icon: str, command: str):
        shell_key = registry.GetKey(*self.reg_path)
        # shell_key


class _ContextMenuType:

    def __init__(self):
        self._open_event = None
        self._return_types = {
            "background": None

        }

    def set_event(self, type_: Literal["background", "file", "directory"]):
        pass


