from typing import Any, Callable
from types import FunctionType


class Event:
    def __init__(self, function: Callable[[Any], Any] = lambda *args, **kwargs: None):
        self.__doc__ = function.__doc__
        if isinstance(function, FunctionType):
            self.__name__ = function.__name__
            self.__annotations__ = function.__annotations__
            self.__defaults__ = function.__defaults__
        self._subs = [function]

    def Subscribe(self, function: callable):
        if isinstance(function, FunctionType):
            if function.__defaults__ != self.__defaults__:
                raise ValueError("This function has the wrong signature.")

        self._subs.append(function)

    def Call(self, *args, **kwargs):
        results = []
        for sub in self._subs:
            r = sub(*args, **kwargs)
            results.append(r)
        return results

    def __iadd__(self, other: callable):
        """
        Implement self += other
        """
        res = self
        res.Subscribe(other)
        return res

    def __call__(self, *args, **kwargs):
        """
        Implement self(*args, **kwargs)
        """
        return self.Call(*args, **kwargs)

