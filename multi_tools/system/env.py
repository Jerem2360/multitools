from importlib import util
from importlib.machinery import ModuleSpec
from typing import overload, Union
from types import FunctionType, MethodType
from threading import Thread
import sys
from multi_tools import arrays


def module_installed(module: str):
    """
    Search for module and return whether it exists.
    """
    if util.find_spec(module) is not None:
        return True
    return False


def import_module(module_name: str):
    """
    Import module programmatically.
    """
    return Module(module_name)


class Handle(object):
    def __init__(self, target_name: str):
        """
        Class that represents Handles.
        A subclass must call Handle.__init__ at **the end** of it's own __init__ definition.
        Since __getattr__ will return target.__getattr__(name), you will have to use safe_getattr(name)
        instead to obtain self.name
        :param target_name: This parameter is the subclass' attribute name whom to handle directly.
        It's attributes will replace the actual object's attributes.

        For an example, see the Module class.
        """
        setattr(self, "_target", target_name)

    def safe_getattr(self, name): return self.__super_getattr__(name)  # used to obtain the object's real attributes

    def __hasattr__(self, item):
        """
        Implement hasattr(super())
        """
        try:
            super().__getattribute__(item)
        except AttributeError:
            return False
        return True

    def __getattr__(self, item):
        """
        Here comes the magic.
        We override getattr(self, item) to give us self.__getattribute__(_target).item
        """
        # if the real self has an attribute called item:
        if self.__hasattr__(item):
            return super().__getattribute__(item)

        # if the handled object (the fake self) has an attribute called item:
        if hasattr(super().__getattribute__(super().__getattribute__("_target")), item):
            target = super().__getattribute__("_target")
            return super().__getattribute__(target).__getattribute__(item)
        # if none of them is found, raise AttributeError with customizable message:
        raise AttributeError(self._attribute_error_message(item))

    def _attribute_error_message(self, item) -> str:
        """
        Customizable AttributeError message.
        """
        return f'{self} has no attribute "{item}"'

    def __super_getattr__(self, name):
        """
        Implement getattribute(super())

        Used to get attributes from the real self.
        """
        return super().__getattribute__(name)

    def __repr__(self):
        target_name = super().__getattribute__("_target")
        return f'<"{target_name}" handle at {hex(id(self))}>'


class Module(Handle):
    @overload
    def __init__(self, module: ModuleSpec): ...

    @overload
    def __init__(self, module: str): ...

    def __init__(self, module=None):
        """
        Create and return a module object. If an existing module is found, gets
        a copy of it.
        """
        self._module = None
        if isinstance(module, ModuleSpec):
            self._module = util.module_from_spec(module)
        elif isinstance(module, str):
            spec = util.find_spec(module)
            if spec is not None:
                self._module = util.module_from_spec(spec)

        Handle.__init__(self, "_module")

    def __repr__(self):
        """
        Implement repr(self)
        """
        return repr(super().__super_getattr__("_module"))

    def __str__(self):
        """
        Implement str(self)
        """
        return str(super().__super_getattr__("_module"))


class thread_(object):
    def __init_subclass__(cls, **kwargs):
        raise TypeError("'thread' class can't be subclassed.")

    def __init__(self, function: FunctionType):
        """
        Create and return a threaded function.
        """
        self._function = function

    def __call__(self, *args, **kwargs):
        """
        Implement self(*args, **kwargs)
        """
        Thread(target=self._function, args=args, kwargs=kwargs).start()


def thread(f: Union[FunctionType, MethodType]):
    def inner(*args, **kwargs):
        th = thread_(f)
        return th(*args, **kwargs)
    return inner


class ThreadContainer:

    def __init_subclass__(cls, start_immediately=False):
        """
        Implement

        class C(cls, start_immediately=False):
        """
        cls._immediate_start = start_immediately

    def __init__(self, args: tuple = None, kwargs: dict = None):
        """
        Superclass for threaded classes.
        """
        self._locked = False
        self._thread = None

        if self._immediate_start:
            if args is None:
                args = ()
            if kwargs is None:
                kwargs = {}
            self.start(*args, **kwargs)

    def _call(self, *args, **kwargs):
        """
        Method that is called at the start of the thread.
        """
        self.main(*args, **kwargs)
        self._locked = False

    def main(self, *args, **kwargs):
        """
        The thread's lifetime, actions.
        You may override this to customize what the thread does.
        """
        pass

    def start(self, *args, **kwargs):
        """
        Method that starts the thread.
        """
        if not self._locked:
            self._locked = True
            self._thread = Thread(target=self._call, args=args, kwargs=kwargs)
            self._thread.start()

    @property
    def thread(self):
        return self._thread

    def __getitem__(self, item):
        if not item.startswith('_'):
            return self._thread.__getattribute__(item)

    @staticmethod
    def print(*args, sep=' ', end='\n', flush=False, file=sys.stdout):
        """
        A cleaner version of print(), but for threads.
        """
        text = ""
        counter = 0
        for word in args:
            word = str(word)
            text += word
            if counter < (len(args) - 1):
                text += sep
        text += end

        file.write(text)
        if flush:
            file.flush()


class ParametrizedDecoratorFunc(object):
    __slots__ = ['_func', '_args', '_kwargs']

    def __init__(self, function: Union[FunctionType, MethodType]):
        """
        Decorator function that can take additional parameters.

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

        func = Decorator(arg1, arg2, arg3)(func)
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


class MethodDecorator:
    dec = lambda f: lambda self: f(self)

    def __init__(self, method: MethodType):
        self.method = method

    def _wrap_with_this(self, *args, **kwargs):
        def wrapped(this):
            self.method(this, *args, **kwargs)

