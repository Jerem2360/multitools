from ctypes import CDLL, WinDLL
from _ctypes import CFuncPtr


CDECL = -1
STDCALL = -2


class CModule(object):

    _call_methods = {
        CDECL: CDLL,
        STDCALL: WinDLL
    }

    __slots__ = ["_dll", "__name__"]

    def __init__(self, path, mode=CDECL):
        DllType = self._call_methods[mode]
        self._dll = DllType(path)
        if '/' in path:
            nm = path.split('/')[-1]
        elif '\\' in path:
            nm = path.split('\\')[-1]
        else:
            nm = path

        self.__name__ = nm

    def __getattr__(self, item):
        try:
            resFunc = self._dll[item]
        except AttributeError:
            self._attr_error(item)
            return  # will never occur since AttributeError is raised
        if isinstance(resFunc, CFuncPtr):
            return resFunc
        self._attr_error(item)
        return  # will never occur since AttributeError is raised

    def _attr_error(self, name):
        raise AttributeError(f"'{self.__name__}' library has no attribute '{name}'.")

    __origin__ = property(lambda self: self._dll)


def c_import(path, mode=CDECL):
    return CModule(path, mode=mode)

