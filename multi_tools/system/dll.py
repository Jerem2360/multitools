from multi_tools.system.env import Handle
import ctypes


class Dll(Handle):
    AnyDll = ctypes.CDLL
    CDll = ctypes.CDLL
    WinDll = ctypes.WinDLL
    PyDll = ctypes.PyDLL

    def __init__(self, path: str, dll_type=AnyDll):

        x = ctypes.LibraryLoader(dll_type)
        self._lib = x.LoadLibrary(path)
        self._path = path

        super().__init__("_lib")

    def __getitem__(self, item):
        return self.__getattribute__(item)

    def _attribute_error_message(self, item):
        return f'Dll file "{self.safe_getattr("_path")}" has no function named "{item}".'

    def __repr__(self):
        path = self.safe_getattr("_path")
        return f'<Handle for dll "{path}" at {hex(id(self))}>'

