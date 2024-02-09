

class ReassignedFunction:
    """
    Replaced version of an existing function inside a module.
    """
    __slots__ = (
        '_base',
        '_new',
        '__weakref__',
    )
    
    def __init__(self, base, new):
        import inspect
        self._base = base
        self._new = new
        try:
            self.__signature__ = inspect.signature(base)
        except:
            pass

    def __call__(self, *args, **kwargs):
        return self._new(self._base, *args, **kwargs)

    def __getattribute__(self, item):
        if item == '__module__':
            return super().__getattribute__('_base').__module__
        return super().__getattribute__(item)

    def __getattr__(self, item):
        return getattr(self._base, item)

    def __repr__(self):
        beginning = self._base.__repr__().removesuffix('>')
        end = '>' if self._base.__repr__().endswith('>') else ''
        return beginning + f", reassigned to {self._new}" + end


def inline_reassign(oldfunc):
    def _inner(newfunc):
        import sys
        module = sys.modules[oldfunc.__module__]
        reassigned = ReassignedFunction(oldfunc, newfunc)
        setattr(module, oldfunc.__name__, reassigned)
        return newfunc
    return _inner


def reassign(oldfunc, newfunc):
    """
    Allows transparently overwriting the behaviour of a given function
    that exists inside a specific module with that of the specified new
    behaviour. The function representing the new behaviour takes an implicit
    first parameter which is the original function, followed by the normal
    sequence of parameters taken by the original function.
    """
    return inline_reassign(oldfunc)(newfunc)


import sys


# original versions of methods from sys that have been reassigned, don't touch!
__sys_setswitchinterval__ = sys.setswitchinterval
__sys_setrecursionlimit__ = sys.setrecursionlimit
__sys_settrace__ = sys.settrace
__sys_gettrace__ = sys.gettrace


@inline_reassign(sys.setswitchinterval)
def _set_switch_interval(base, value):
    from . import interp
    interp_status = interp.Interpreter.current._status
    base(value)
    if interp_status.switch_interval.acquire():
        interp_status.switch_interval.update(value)
        interp_status.switch_interval.release()


@inline_reassign(sys.setrecursionlimit)
def _set_recursion_limit(base, value):
    from . import interp
    interp_status = interp.Interpreter.current._status
    base(value)
    if interp_status.recursion_limit.acquire():
        print('here', value)
        interp_status.recursion_limit.update(value)
        interp_status.recursion_limit.release()


def _settrace(base, trace_func):
    print("custom settrace")
    from . import execution_loop
    import _thread
    execution_loop.ExecutionLoop.__wrapped__[_thread.get_ident()] = trace_func


def _gettrace(base):
    from . import execution_loop
    import _thread
    return execution_loop.ExecutionLoop.__wrapped__.get(_thread.get_ident(), None)

