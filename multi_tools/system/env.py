from importlib import util
from importlib.machinery import ModuleSpec
from typing import overload
from types import FunctionType
from threading import Thread
import sys


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


class thread(object):
    def __init__(self, function: FunctionType):
        self._function = function

    def __call__(self, *args, **kwargs):
        Thread(target=self._function, args=args, kwargs=kwargs).start()

    @staticmethod
    def print(*args, sep=' ', end='\n', flush=False, file=sys.stdout):
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

