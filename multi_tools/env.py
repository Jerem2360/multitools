from importlib import util
from importlib.machinery import ModuleSpec
from typing import overload

def define(name: str, value):
    globals()[name] = value


def module_installed(module: str):
    if util.find_spec(module) is not None:
        return True
    return False


def import_module(module_name: str):
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
        Make a variable with
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
        return repr(super().__super_getattr__("_module"))

    def __str__(self):
        return str(super().__super_getattr__("_module"))