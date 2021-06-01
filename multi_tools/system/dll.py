from multi_tools.system.env import Handle
import ctypes


class Dll(Handle):
    AnyDll = ctypes.CDLL
    CDll = ctypes.CDLL
    WinDll = ctypes.WinDLL
    PyDll = ctypes.PyDLL

    def __init__(self, path: str, dll_type=AnyDll):
        self.type = dll_type
        self.path = path

        x = ctypes.LibraryLoader(self.type)
        self._lib = x.LoadLibrary(self.path)
        del self.type
        del self.path
        super().__init__("_lib")


