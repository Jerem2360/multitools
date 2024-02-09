import os
import sys
from .._internal import *


_module_unhidables = (
    '__dict__',
    '__name__',
    '__loader__',
    '__package__',
    '__spec__',
    '__path__',
    '__file__',
    '__cached__',
    '__code__',
    '__annotations__',
    '__dir__',
)


class MultitoolsModule(type(sys)):
    def __init__(self, name, code, **kwargs):
        super().__init__(name, doc=kwargs.pop('doc', None))
        self.__code__ = code
        self.__name__ = name
        super().__setattr__('__private__', kwargs.pop('private', []))

        if 'file' in kwargs:
            self.__file__ = kwargs.pop('file')

        if len(kwargs):
            raise TypeError(f"Unexpected keyword argument{'s' if len(kwargs) > 1 else ''} "
                            f"{repr(tuple(kwargs.keys()))[1:-1].removesuffix(',')}.")

    def __getattribute__(self, item):
        if item in _module_unhidables:
            return super().__getattribute__(item)

        private = super().__getattribute__('__private__').copy()
        private.append('__private__')
        if item in private:
            raise AttributeError(f"module '{self.__name__}' has no public attribute '{item}'.")
        return super().__getattribute__(item)

    def __setattr__(self, key, value):
        if key in _module_unhidables:
            return super().__setattr__(key, value)

        private = super().__getattribute__('__private__').copy()
        private.append('__private__')
        if key in private:
            raise AttributeError(f"module '{self.__name__}' has no public attribute '{key}'.")
        return super().__setattr__(key, value)

    def __dir__(self):
        res = list(self.__dict__.keys())
        private = super().__getattribute__('__private__').copy()
        private.append('__private__')
        for priv in private:
            try:
                res.pop(res.index(priv))
            except ValueError:
                pass
        return res

    def __exec__(self, __locals=None, /):
        return exec(self.__code__, self.__dict__, __locals)


class MultitoolsModuleSpec:
    pass


class MultitoolsImporter:
    def __init__(self):
        pass

    def find_spec(self, name, path, target=None):
        relname = name.split('.')[-1]

        if __GLOBAL_NAME__ not in name:
            return

        file = None
        if path is None:
            path = sys.path
        for p in path:
            if not os.path.exists(p):
                continue
            for filename in os.listdir(p):
                if filename in (relname + '.py', relname + '.pyi'):
                    file = p + os.path.sep + filename

        if file is None:
            return

        spec = MultitoolsModuleSpec()
        spec.name = name
        spec.loader = self
        spec.origin = file
        spec.submodule_search_locations = None
        spec.loader_state = None
        spec.cached = None
        spec.parent = '.'.join(name.split('.')[:-1]) if len(name.split('.')) > 1 else ''
        spec.has_location = True
        return spec

    def create_module(self, spec):
        private = []
        with open(spec.origin, 'r') as fs:
            contents = fs.read()
            lines = contents.splitlines()

        for line in lines:
            if line.startswith('#private '):
                dummy, name = line.split(' ')
                private.append(name)

        code = compile(contents, spec.origin, 'exec', dont_inherit=True)

        res = MultitoolsModule(spec.name, code, private=private)
        res.__spec__ = spec
        return res

    def exec_module(self, module):
        if isinstance(module, MultitoolsModule):
            return module.__exec__()

        with open(module.__spec__.origin, 'r') as fs:
            contents = fs.read()

        exec(contents, module.__dict__)


sys.meta_path.insert(-2, MultitoolsImporter())


