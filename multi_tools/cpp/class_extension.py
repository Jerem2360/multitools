import ctypes
import os
from multi_tools import config, common, functional
from types import FunctionType


if not os.path.exists(config.Cpp.APPDATA):
    os.mkdir(config.Cpp.APPDATA)


def search_dll(name: str) -> ctypes.CDLL:
    """
    Utility for searching .dll libraries.
    """
    for path in config.Cpp.search_paths:
        if os.path.exists(path + name) and name.endswith('.dll'):
            return config.Cpp.dll_type(path + name)
    raise ReferenceError(f"Failed to solve external reference '{name}' in {tuple(config.Cpp.search_paths)}.")


def search_method(dll: ctypes.CDLL, name: str):
    """
    Utility for searching specific functions inside a .dll library.
    """
    if hasattr(dll, name):
        return getattr(dll, name)
    raise ReferenceError(f"Failed to solve external reference '{name}' in library {dll}.")


class _Header:

    return_type_logic = {
        int: ctypes.c_long,
        float: ctypes.c_double,
        str: ctypes.c_char_p,
        bool: ctypes.c_bool,
        None: None
    }

    def __init__(self, function: FunctionType):
        """
        A support class for header functions.
        **Internal use only**
        """

        self._func = function

        def _wrap(self_or_cls, *args):
            if not hasattr(self_or_cls, '__dll__'):
                raise TypeError("Owner class must be decorated with '@HeaderClass(dll_name).'")
            function_name: str = self._func.__name__
            if function_name.startswith('__') and function_name.endswith('__'):

                true_name = function_name.removeprefix('__').removesuffix('__')
                return self.wrapper_special(true_name, self_or_cls, *args)

            else:
                return self.wrapper_normal(function_name, self_or_cls, *args)

        _wrap = functional.copy_function_data(function, _wrap)
        return_type = function.__annotations__.get("return")
        self.func = _wrap
        self.func.restype = self.return_type_logic[return_type]
        print(self.func.restype)

    @staticmethod
    def wrapper_special(name, self_or_cls, *args):
        c_func = search_method(self_or_cls.__dll__, f"PySpecial_{name}")
        _args = [common.Dll.basic_type_wrap(a) for a in args]
        args = tuple(_args)
        self_or_cls = common.Dll.wrap_self(self_or_cls)
        res = c_func(self_or_cls, *args)
        if res is not None:
            if name == "init":
                # print(res, type(res))
                return None
            return common.Dll.basic_type_unwrap(res)

    @staticmethod
    def wrapper_normal(name, self_or_cls, *args):
        c_func = search_method(self_or_cls.__dll__, f"Py_{name}")
        _args = [common.Dll.basic_type_wrap(a) for a in args]
        args = tuple(_args)
        self_or_cls = common.Dll.wrap_self(self_or_cls)
        res = c_func(self_or_cls, *args)
        if res is not None:
            return common.Dll.basic_type_unwrap(res)


def HeaderFunc(func):
    """
    If the owner class is decorated with @HeaderClass , decorated function will be replaced by
    the corresponding function of the dll that was specified to the class
    decorator. If the owner class is not correctly decorated, TypeError is raised.

    -> return type: '_ctypes.FuncPtr'

    -> possible raised errors: ReferenceError, TypeError

    The right dll function is chosen depending on the header
    function's name. Please note that static methods are not compatible with this system.
    If you plan to use static methods coming from .dlls, consider
    using the @system.DllImport decorator instead.

    - If the function is a classic function, the decorator will look in the dll
        for a function named after "Py_<name>", where 'name' is the name of the
        header function; and replace it.

    - If the function is a special function like __init__ or __bool__, on the other
        hand, the decorator would look for a function named "PySpecial_<name>" with
        'name' being the header function's name without the '_' characters.

    For example, if you were to make a header function called "foo", a function
    called "Py_foo" would be searched inside the .dll library.

    If you were to make your "__init__" function a header, a function called
    "PySpecial_init" would be searched inside the .dll library.

    If the function happens to not be exported by the .dll, python wouldn't find it
    and a ReferenceError will be raised.


    Note:

    When the decorator replaces the header function, it keeps it's name, dotted name,
    documentation, annotations (signature), and parent module reference, and copies
    them into the new function object that comes from the dll.

    For this reason, you should make sure to have the function's accurate signature
    given to the header function, otherwise, at runtime, it won't be stored anywhere.


    Other note:

    Multiple classes can inheritate from the same .dll library.
    """
    _h = _Header(func)
    return _h.func


@functional.DecoratorWithParams
def HeaderClass(cls: type, dll: str, type_: type[ctypes.CDLL] = ctypes.CDLL):
    """
    -> Parameters:
        dll: 'os.pathlike'
        type_: type[ctypes.CDLL]

    -> return type: 'type'

    -> Possible raised errors: ReferenceError

    Class decorator that makes a class capable of supporting @HeaderFunc functions.
    It's member functions that are declared with @HeaderFunc will be replaced by
    a function from 'dll' that is named:
        - "Py_<function name>" for normal functions
        - "PySpecial_<name without underscores>" for special functions like __init__

    See 'HeaderFunc' for more details.

    See example in 'system.memory.Pointer'.
    """
    config.Cpp.dll_type = type_
    cls.__dll__ = search_dll(dll)
    return cls
