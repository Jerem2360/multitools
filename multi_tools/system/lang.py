from multi_tools import system
from types import FunctionType


@system.DecoratorWithParams
def functionof(func: callable, obj, globals_):
    for obj_ in globals_():
        if obj_ == obj:
            obj_.__setattr__(func.__qualname__, func)


def staticclass(cls):
    class StaticMClass(type):
        def __new__(mcs, name, bases=(object,), dict_=None):

            if dict_ is None:
                dict_ = {}

            def __init__(self, *_args, **_kwargs):
                pass

            def __init_subclass__(_cls_, **_kwargs):
                _cls_.__init__ = lambda self, *a, **kw: None

            return super().__new__(mcs, name, bases, {'__init__': __init__, '__init_subclass__': __init_subclass__, **dict_})

    return StaticMClass(cls.__name__)


@staticclass
class Bytes:
    @staticmethod
    def from_id(id_: int) -> str:
        h = str(hex(id_)).split('0x')[-1]
        r = '0x' + h.upper()
        return r


class MutableType:

    def __init__(self):
        super().__setattr__('_tp', type('_tp', (object,), {}))

    def methoddef(self, func: FunctionType):
        _tp = super().__getattribute__('_tp')
        _tp.__setattr__(_tp, func.__qualname__, func)
        super().__setattr__('_tp', _tp)

    def __getattr__(self, item):
        _tp = super().__getattribute__('_tp')
        return _tp.__getattr__(item)

    def __setattr__(self, key, value):
        _tp = super().__getattribute__('_tp')
        _tp.__setattr__(_tp, key, value)
        super().__setattr__('_tp', _tp)

    def __call__(self, *args, **kwargs):
        _tp = super().__getattribute__('_tp')
        return _tp(*args, **kwargs)


