import os
import sys
from typing import Callable, overload
from types import TracebackType

from . import tstate


_ExceptHook = Callable[[type[BaseException], BaseException, TracebackType | None], None]


Interpreter: "_PyInterpreter" = ...
"""
Immortal object representing the current state of the python interpreter.
Most things in here are already exposed through the sys and os modules, but
storing everything in the same place seems more convenient.
"""


class _Version:
    @overload
    def __init__(self, *nums: int, _type: str = ..., _serial: int = ...): ...
    @overload
    def __init__(self, strversion: str, /, *, _type: str = ..., _serial: int = ...): ...

    def __init__(self, *args, _type="release", _serial=0):
        self._type = _type
        self._serial = _serial
        if len(args) == 1 and isinstance(args[0], str):
            self._numbers = tuple(int(n) for n in args[0].split('.'))
            return
        if len(args):
            self._numbers = tuple(arg.__index__() for arg in args)


    def __getitem__(self, item):
        return self._numbers[item]

    @property
    def type(self):
        return self._type

    @property
    def serial(self):
        return self._serial

    def __iter__(self):
        return iter(self._numbers)

    def __repr__(self):
        return f"version(\"{'.'.join(self._numbers)}\", {self._type}, {self._serial})"


class _PyInterpreter:
    """
    Wraps the current python interpreter state.
    This type is immortal and can only be instantiated once.
    Instantiating it further will just return the object previously created.
    """
    _cache = None

    TState = tstate.TState

    def __new__(cls,
                __finalizer=lambda *args, **kwargs: None,
                __trace=lambda *args, **kwargs: None,
                __excepthook=lambda exc_type, exc_value, tb: None,
                *args, **kwargs):
        if cls._cache is not None:
            return cls._cache
        self = super().__new__(cls)
        import sys
        if sys.implementation.name != 'cpython':
            return self
        import _ctypes

        # make our object immortal:
        _ctypes.Py_INCREF(self)

        # register the finalizer:
        import weakref
        weakref.finalize(self, __finalizer)

        # register the main thread:
        def tracefunc(f, e, a):
            # print("calling trace")
            __trace(f, e, a)
            return tracefunc

        """ts = tstate.TState.current()
        tstate.make_tracefunc(ts, tracefunc)"""

        # register currently alive threads:
        import threading
        from . import __init_thread__
        for th in threading.enumerate():
            __init_thread__(tstate.TState(th.ident))

        # update sys.excepthook:
        import sys
        self._excepthook = sys.excepthook

        sys.excepthook = __excepthook

        return self

    def __init_subclass__(cls, **kwargs):
        raise TypeError("class '_PyInterpreter' is not a base class.")

    @property
    def finalizing(self):
        import sys
        return sys.is_finalizing()

    @property
    def flags(self):
        import sys
        return sys.flags

    @property
    def recursion_limit(self):
        import sys
        return sys.getrecursionlimit()

    @recursion_limit.setter
    def recursion_limit(self, value: int):
        import sys
        sys.setrecursionlimit(value)

    @property
    def switch_interval(self):
        import sys
        return sys.getswitchinterval()

    @switch_interval.setter
    def switch_interval(self, value: float):
        import sys
        sys.setswitchinterval(value)

    @property
    def argv(self):
        import sys
        return sys.argv

    @property
    def module_cache(self):
        import sys
        return sys.modules

    @property
    def stdlib_modules(self):
        import sys
        return sys.stdlib_module_names

    @property
    def implementation(self):
        import sys
        return sys.implementation

    @property
    def version(self):
        return _Version(sys.version_info.major,
                        sys.version_info.minor,
                        sys.version_info.micro,
                        _type=sys.version_info.releaselevel,
                        _serial=sys.version_info.serial,
                        )

    @property
    def sysmodule(self):
        import sys
        return sys

    @property
    def builtinsmodule(self):
        import builtins
        return builtins

    @property
    def threads(self) -> tuple[int]:
        return tuple(type(self).TState._cache.values())

    @property
    def excepthook(self) -> _ExceptHook:
        return self._excepthook

    @excepthook.setter
    def excepthook(self, value: _ExceptHook):
        self._excepthook = value

    def __repr__(self):
        return "<Python interpreter>"


import os

