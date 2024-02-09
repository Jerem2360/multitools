from typing import TypeVar, Generic

from .features import *


def _get_proxy(proxy):
    res = proxy.__get_value__()
    if res is NotImplemented:
        return proxy.__cache__
    proxy.__cache__ = res


class Proxy:
    def __init__(self):
        self.__cache__ = self.__get_value__()

    def __get_value__(self):
        return

    def __getattribute__(self, item):
        if item in ('__get_value__', '__dict__', '__cache__'):
            return super().__getattribute__(item)
        if item.startswith('__') and item.endswith('__'):
            return getattr(self.__get_value__(), item)
        if item in self.__dict__:
            return super().__getattribute__(item)
        return getattr(self.__get_value__(), item)

    def __repr__(self):
        return f"<proxy [{repr(self.__get_value__()).removeprefix('<').removesuffix('>')}]>"


print(Proxy())


class TState:
    _objects = {}

    __slots__ = (
        '_init',
        '_id'
    )

    def __new__(cls, tid):
        if tid in cls._objects:
            return cls._objects[tid]
        self = super().__new__(cls)
        self._init = False
        self._id = tid
        cls._objects[tid] = self
        return self

    def __init__(self, *args, **kwargs):
        if self._init:
            return
        self._init = True

    @classmethod
    def current(cls):
        import _thread
        return cls(_thread.get_ident())

