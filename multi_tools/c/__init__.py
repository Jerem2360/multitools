from . import c_module
from os import PathLike


class modes:
    CDECL = c_module.CDECL
    STDCALL = c_module.STDCALL


def c_import(path: PathLike, mode: int = modes.CDECL) -> c_module.CModule:
    return c_module.c_import(path, mode=mode)

