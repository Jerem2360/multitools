from ._internal.protocols import *


def abspath_from_moddir(path):
    from ._internal.interp import Interpreter
    import os
    temp_curdir = os.curdir
    tstate = Interpreter.TState.current()
    caller_dir = tstate.call_stack[1].f_code.co_filename.rsplit(os.path.sep, 1)[0]
    os.chdir(caller_dir)
    res = os.path.abspath(path)
    os.chdir(temp_curdir)
    return res


def override_curdir(path) -> ContextManager:
    """
    Returns a context manager that changes the current working
    directory to the specified path only inside its scope.
    """
    from ._internal.runtime import CurdirOverride
    return CurdirOverride(path)


def curdir_at_module_location() -> ContextManager:
    """
    Returns a context manager that changes the current working
    directory to the current file's location only inside its
    scope. Useful for modules that are imported but not executed
    directly.
    """
    from ._internal.runtime import curdir_at_module_location as base
    return base(1)

