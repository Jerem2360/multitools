import sys

__import__('', globals(), fromlist=[
    'interp',
], level=1)



def __initialize__():
    from .interp import _PyInterpreter
    from . import interp
    from . import trace, exc_handling
    from .tstate import TState

    interp.Interpreter = _PyInterpreter(__finalize_thread__, trace.__trace__, exc_handling.excepthook)


def __init_thread__(state):
    from . import trace, tstate, exc_handling
    tstate.make_tracefunc(state, trace.__trace__)
    state.add_trace(exc_handling.trace_exceptions, event='exception')
    state._do_trace = True
    state._do_events = True


def __finalize_thread__():
    from .interp import Interpreter
    import _thread
    try:
        del Interpreter.TState._cache[_thread.get_ident()]
    except KeyError:
        pass

