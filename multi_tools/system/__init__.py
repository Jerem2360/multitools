import sys
if sys.platform == 'win32':
    from multi_tools.system import registry, dll
from multi_tools.system import env, runtime, memory
from time import sleep as _slp


thread = runtime.thread

import_module = env.import_module

if sys.platform == 'win32':
    DLL = dll.Dll


    class dlls:
        _system32 = 'C:/windows/system32'
        msvcrt = dll.Dll(_system32 + '/msvcrt.dll', dll_type=dll.Dll.WinDll)
        user32 = dll.Dll(_system32 + '/user32.dll', dll_type=dll.Dll.CDll)
        kernel32 = dll.Dll(_system32 + '/kernel32.dll', dll_type=dll.Dll.WinDll)
        devinv = dll.Dll(_system32 + '/devinv.dll', dll_type=dll.Dll.WinDll)
        devmgr = dll.Dll(_system32 + '/devmgr.dll', dll_type=dll.Dll.WinDll)


def wait(time_secs: int or float):
    return _slp(time_secs)


class Module(env.Module):
    @staticmethod
    def is_installed(name: str):
        return env.module_installed(name)


DllImport = dll.DllImport


Thread = runtime.ThreadContainer


try:
    addressof = memory.addressof
except AttributeError:
    pass
