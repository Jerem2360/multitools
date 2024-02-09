"""
Tells if some common useful functionalities are present in the current interpreter.
"""


__available_modules__ = {}
"""A non-exhaustive list of implementation-specific modules that are present in the interpreter."""


def _test_module(name):
    try:
        mod = __import__(name)
    except ImportError:
        return False

    __available_modules__[name] = mod
    return True


EXCEPT_ALL = __import__('sys').version_info >= (3, 11, 4)
MATCH_STMT = __import__('sys').version_info >= (3, 10)
PYSIDE_BUFFERS = INLINE_GENERICS = __import__('sys').version_info >= (3, 12)  # in prevision to incoming python 3.12
FORK_SYSCALL = hasattr(__import__('os'), 'fork')


SIGNAL_MODULE = _test_module("signal")  # its presence indicates that signal handling is done by the interpreter.
WINAPI_MODULE = _test_module("_winapi")  # only for windows
POSIXSUBPROCESS_MODULE = _test_module("_posixsubprocess")  # for posix platforms only
CCTYPES_MODULE = _test_module("_ctypes")  # may not be available everywhere
WINREG_MODULE = _test_module("winreg")  # only for Windows
TKINTER_MODULE = _test_module("tkinter")  # tcl/tk is an optional feature of python
THREADING_MODULE = _test_module("threading")  # this isn't available in Emscripten or in WASI
THREAD_MODULE = _test_module("_thread")
NT_MODULE = _test_module('nt')
POSIX_MODULE = _test_module('posix')

