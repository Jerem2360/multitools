from typing import Union
from types import FunctionType, MethodType


class ParametrizedDecoratorFunc(object):
    __slots__ = ['_func', '_args', '_kwargs']

    def __init__(self, function: Union[FunctionType, MethodType]):
        """
        Decorator that gives decorated functions the ability
        to take multiple parameters whilst decorating other functions
        or classes.

        It could be used to give some decorators unique properties.

        e.g:

        @ParametrizedDecoratorFunc
        def example(f: Union[FunctionType, MethodType], name: str):

            f.__globals__['custom_name'] = name

            return f


        @example('Test')
        def test():
            print(custom_name)


        test()


        >> Test
        """
        self._func = function

    def __call__(self, *args, **kwargs):
        """
        Implement self(*args, **kwargs)

        Calling self as non decorator can cause weird bugs if not done as so:

        func = Decorator(arg1, arg2, ...)(func)
        """
        # store args and kwargs in self so the wrapper can access them:
        self._args = args
        self._kwargs = kwargs
        return self._wrap

    def _wrap(self, f: Union[FunctionType, MethodType]):
        """
        The function's wrapper.
        The actual 'decorator' that is applied to the
        decorated function.
        """
        # call _func with function to decorate / additional parameters, and return:
        return self._func(f, *self._args, **self._kwargs)

    def __getattr__(self, item):
        """
        Implement getattr(self).

        If a function-specific attribute is asked, return the target's
        attribute (self._func).
        Otherwise, just return self's right attribute.
        """
        external = False
        if not hasattr(self._func, '__code__'):
            external = True
        if item == 'external':
            return external

        if not hasattr(self._func, '__code__'):
            # accessible values of the function if it is external:
            possibilities = {
                '__name__': self._func.__name__,
                '__qualname__': self._func.__qualname__,
                '__annotations__': self._func.__annotations__,
                '__globals__': self._func.__globals__,
                '__doc__': self._func.__doc__
            }
        else:
            # accessible values of the function if it is internal:
            possibilities = {
                '__qualname__': self._func.__qualname__,
                '__annotations__': self._func.__annotations__,
                '__defaults__': self._func.__defaults__,
                '__code__': self._func.__code__,
                '__name__': self._func.__name__,
                '__closure__': self._func.__closure__,
                '__globals__': self._func.__globals__,
                '__doc__': self._func.__doc__
            }

        if item in possibilities:
            return possibilities[item]
        return super().__getattribute__(item)

    @property
    def unwrapped(self):
        """
        An unwrapped version of the function.
        """
        return self._func

    def __repr__(self):
        return "<Special Decorator \"{0}\" at {1}>".format(self._func.__qualname__, str(hex(id(self))).upper())
