import sys
if sys.platform == 'win32':
    from multi_tools.system import registry, dll
from multi_tools.system import env, functional, runtime
from multi_tools.system.generics import optional
from time import sleep as _slp
import os


thread =runtime.thread

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


    class dllgroup:
        def __init__(self, source_path: str):
            if not os.path.exists(source_path):
                raise NotADirectoryError(f"Unable to find directory '{source_path}'.")
            self.path = source_path

        def add(self, dllname: str):
            self.__setattr__(dllname, dll.Dll(self.path + '/' + dllname + '.dll', dll_type=dll.Dll.AnyDll))


def wait(time_secs: int or float):
    return _slp(time_secs)


class Module(env.Module):
    @staticmethod
    def is_installed(name: str):
        return env.module_installed(name)


DecoratorWithParams = env.ParametrizedDecoratorFunc
DllImport = dll.DllImport


Thread = runtime.ThreadContainer


class Functional:
    @staticmethod
    def lambda_(code, *args): return functional.lambda_statement(code, *args)

