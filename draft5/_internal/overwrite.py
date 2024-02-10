import sys as _sys
import _thread


def _unsafe_overwrite(old):
    def _inner(new):
        overwritten = OverwrittenFunction(old, new)
        parent = _sys.modules[old.__module__]
        name = old.__qualname__.split('.')[-1]
        nodes = old.__qualname__.split('.')[:-1]

        for node in nodes:
            parent = getattr(parent, node)

        setattr(parent, name, overwritten)
        return overwritten

    return _inner


class OverwrittenFunction:
    """
    Implements the behaviour of a function that has been overwritten.
    Uses the behaviour of the overwritten version.
    Has the attributes from the old version as well as the ones from
    the overwritten version. Apart for __code__, attributes from the
    original version have precedence over the ones from the overwritten
    version.
    """

    __slots__ = (
        '_base',
        '_new',
        '__weakref__',
    )

    def __init__(self, base, new):
        self._base = base
        self._new = new

    def __getattr__(self, item):
        if item == '__code__':
            return getattr(self._new, '__code__')

        if item in ('_base', '_new'):
            return super().__getattribute__(item)

        try:
            return getattr(self._base, item)
        except BaseException as e:
            try:
                return getattr(self._new, item)
            except:
                raise e from e.__cause__  # suppress the second exception, which would have had the first one as a cause. Just raise the first one.

    def __setattr__(self, key, value):
        if key == '__code__':
            return setattr(self._new, '__code__', value)

        if key in ('_base', '_new'):
            return super().__setattr__(key, value)

        try:
            return setattr(self._base, key, value)
        except BaseException as e:
            try:
                return setattr(self._new, key, value)
            except:
                raise e from e.__cause__  # same as for __getattr__

    def __call__(self, *args, **kwargs):
        return self._new(self._base, *args, **kwargs)

    def __repr__(self):
        return "<overwritten " + repr(self._base).removeprefix('<')

    def __dir__(self):
        res = {'_base', '_new', *dir(self._new), *dir(self._base)}  # using a set to avoid having twice the same name
        return list(res)


@_unsafe_overwrite(_sys.gettrace)
def _my_gettrace(base):
    return base()


@_unsafe_overwrite(_sys.settrace)
def _my_settrace(base, tracefunc, /):
    return base(tracefunc)


@_unsafe_overwrite(_thread.start_new_thread)
def _my_start_new_thread(base, function, args, kwargs=None):
    from . import tstate

    tid = base(function, args, kwargs=kwargs)

    while tid not in _sys._current_frames():
        pass
    tstate.TState(tid, _sys._current_frames()[tid])

    return tid

