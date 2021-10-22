from multi_tools.system.env import Handle
from multi_tools import common, functional
from typing import Union
from types import MethodType, FunctionType
import ctypes
import sys
from os import PathLike


if sys.platform != 'win32':
    raise NotImplementedError('This library works only on Windows!')


VoidPointer = ctypes.c_void_p
Array = ctypes.Array


class Dll(Handle):
    AnyDll = ctypes.CDLL
    CDll = ctypes.CDLL
    WinDll = ctypes.WinDLL
    PyDll = ctypes.PyDLL

    def __init_subclass__(cls, **kwargs):
        raise TypeError("'Dll' class can't be subclassed.")

    def __init__(self, path: str, dll_type=AnyDll):
        """
        Initialize a new dll handle for path.
        No type hints are created for its functions,
        if you want to create some, you shall use DllImport.
        """

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
        return f'<Handle for dll "{path}" at {hex(id(self)).upper()}>'

    @staticmethod
    def HasFunc_NoBody(f: Union[FunctionType, MethodType]) -> bool:
        """
        Return whether f() has not declared a body,
        in other words, if it does nothing.
        """
        if f.__code__.co_code == b'd\x01S\x00':  # bytecode for doc and empty code
            return True
        if f.__code__.co_code == b'd\x00S\x00':  # bytecode for empty code
            return True
        return False


@functional.DecoratorWithParams
def DllImport(func: Union[FunctionType, MethodType], file: Union[str, PathLike], type_: type[Dll.AnyDll] = Dll.WinDll):
    """
    Function decorator that implements dll functions
    with custom type hints and documentation.

    This method is similar to the C# method System.Runtime.InteropServices.DllImport().

    Decorated functions must have not declared any body
    and have the name of the wanted dll's function.

    e.g:

    class Msvcrt:
        @staticmethod
        @DllImport("C:/windows/system32/msvcrt.dll")
        def printf(text: bytes, mode: system.optional[int]): ...

    Msvcrt.printf(b'a')

    >>a

    Decorated functions can't take keyword arguments, since
    dll functions never do. To represent optional arguments,
    use system.optional as showed above.

    This syntax is only a user-made type hint for dll functions.

    If you don't need it, please use the 'Dll' class directly.
    """
    dll = Dll(file, type_)
    name = func.__name__
    dll_name = file.split('/')[-1]

    if not hasattr(dll, name):
        # if the function is not found in dll:
        raise AttributeError("Dll \"{0}\" has no function named \"{1}\".".format(dll_name, name))

    def new_function(*args):
        _func = getattr(dll, name)
        _args = [common.Dll.basic_type_wrap(a) for a in args]
        args = tuple(_args)
        res = _func(*args)
        return common.Dll.basic_type_unwrap(res)

    if func.__defaults__ is not None:
        # if keyword arguments are found in the decorated function:
        raise SystemError("Dll functions don't have keyword arguments.")

    if not Dll.HasFunc_NoBody(func):
        # if decorated function declared a body:
        raise SystemError("A dll hint function can't declare a body.")

    new_function.__doc__ = func.__doc__

    return new_function

