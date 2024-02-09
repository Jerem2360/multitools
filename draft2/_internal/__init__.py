
__all__ = (
    '__GLOBAL_NAME__',
    '__INTERNAL_NAME__',
    'Interpreter'
)


from .. import __name__ as __GLOBAL_NAME__
from . import features

__INTERNAL_NAME__ = __name__

class Interpreter:

    __DEBUG__ = not __import__('sys').flags.optimize

    from .runtime import TState

