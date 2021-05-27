from importlib import util
from importlib.machinery import ModuleSpec
from typing import overload
from types import FunctionType
from threading import Thread
from multi_tools.errors.exceptions import PropertyError
import sys
import time


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
        # if none of them is found, just return None:
        return None

    def __super_getattr__(self, name):
        """
        Implement getattribute(super())

        Used to get attributes from the real self.
        """
        return super().__getattribute__(name)


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


class _DummyThread:
    ident = None
    name = None

    def __init__(self):
        pass

    def join(self):
        raise Exception()


class thread(object):
    def __init__(self, function: FunctionType):
        """
        This class is a function decorator that transforms "function" into a thread.
        This thread can then be called as if it were a function, except for class methods,
        that need to be passed manually the self argument.
        Additionally, threads can't return anything.

        """
        self._function = function
        self._thread = _DummyThread()

    def __call__(self, *args, **kwargs):
        """
        Implement self()
        """
        self._not_implemented()

        self._thread = Thread(target=self._function, args=args, kwargs=kwargs).start()

    def join(self):
        """
        Implement self._thread.join()
        """
        self._thread.join()

    def _not_implemented(self):
        """
        Internal method to check for builtin overrides.
        """
        # get name of function:
        func_name = self._function.__qualname__.split(".")[len(self._function.__qualname__.split(".")) - 1]
        
        # if the function is of type __*__, consider it a builtin override:
        if func_name.startswith("__") and func_name.endswith("__"):
            raise NotImplementedError(f"Function \"{func_name}()\" cannot be a thread, because it is considered a builtin override.")

    @staticmethod
    def print(text, *args, end="\n", file=sys.stdout, sep=""):
        """
        Print text and args, separated by sep and followed by end, to file.
        More efficient and reliable than builtin print() inside threads.

        - end defaults to "\\\\n"
        - file defaults to sys.stdout
        - sep defaults to ""
        """
        time.sleep(0.000001)
        to_write = str(text)
        for item in args:
            to_write += sep
            to_write += str(item)

        file.write(to_write + end)


class ThreadContainer:

    def __init__(self, callable_: bool, name=None):
        self._name = name
        self._thread = _DummyThread()
        self._running = False
        self._callable = callable_
        self._target = self.main

    def main(self, *args, **kwargs):
        pass

    def _exec(self, *args, **kwargs):
        self._running = True
        self._target(*args, **kwargs)
        self._running = False

    def start(self, *args, **kwargs):
        self._thread = Thread(name=self._name, target=self._exec, args=args, kwargs=kwargs)
        self._thread.start()
        time.sleep(0.1)

    def __call__(self, *args, **kwargs):
        if self._callable:
            self.start(*args, **kwargs)
            return
        func_name = self._target.__qualname__.split(".")[len(self._target.__qualname__.split(".")) - 1]
        raise AttributeError(f"Initializer \"{func_name}\" of class \"{self.__class__.__name__}\" is not callable.")

    def __getitem__(self, item):
        if item == 'name':
            return self._thread.name
        if item == 'running':
            return self._running
        if item == 'callable':
            return self._callable
        if item == 'id':
            return self._thread.ident

        if not isinstance(item, str):
            raise PropertyError(f"Class \"{self.__class__.__name__}\" has no property named \"{str(item)}\".")

        if hasattr(self._thread, item) and (not item.startswith('_')):
            return self._thread.__getattribute__(item)

        raise PropertyError(f"Class \"{self.__class__.__name__}\" has no property named \"{item}\".")


