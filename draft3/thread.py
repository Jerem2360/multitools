from typing import Callable
from ._internal.tstate import TState
from ._internal.runtime import ScheduledResult


def threadsafe(func: Callable[..., ...]):
    """
    Mark a function as protected against thread concurrency.
    """
    return func


class invokable:
    def __init__(self, func: Callable[..., ...]):
        import inspect
        self._wrapped = func
        self._signature = inspect.signature(func)

    def __call__(self, *args, **kwargs):
        return self._wrapped(*args, **kwargs)

    def __getattr__(self, item):
        from ._internal.exc_handling import FrameMask

        with FrameMask():
            return getattr(self._wrapped, item)

    @property
    def __wrapped__(self):
        return self._wrapped

    @property
    def __signature__(self):
        return self._signature


_ThreadTarget = Callable[[TState, ...], None]


class ThreadDefinition:
    def __init__(self, func: _ThreadTarget):
        from ._internal import tstate
        tstate.check_threadfunc_valid_signature(func)
        self._wrapped = func
        self._signature = tstate.get_threadfunc_signature(func)

        if hasattr(func, '__name__'):
            self.__name__ = func.__name__
        if hasattr(func, '__qualname__'):
            self.__qualname__ = func.__qualname__
        if hasattr(func, '__module__'):
            self.__module__ = func.__module__
        if hasattr(func, '__code__'):
            self.__code__ = func.__code__
        if hasattr(func, '__defaults__'):
            self.__defaults__ = func.__defaults__
        if hasattr(func, '__kwdefaults__'):
            self.__kwdefaults__ = func.__kwdefaults__
        self.__annotations__ = getattr(func, '__annotations__', None)
        self.__doc__ = getattr(func, '__doc__', None)

    def __call__(self, *args, **kwargs):
        import _thread
        import sys
        from ._internal import exc_handling, __init_thread__, __finalize_thread__

        alive_lock = _thread.allocate_lock()
        startsync_lock = _thread.allocate_lock()

        def _inner():
            tstate = TState.current()
            alive_lock.acquire()
            startsync_lock.release()

            __init_thread__(tstate)

            try:
                with exc_handling.FrameMask():
                    self._wrapped(tstate, *args, **kwargs)
            except:
                print(f"Exception in thread {tstate.id}:", file=sys.stderr)
                sys.excepthook(*sys.exc_info())

            tstate._do_trace = False
            while len(tstate._event_queue):
                tstate._event_queue[-1].run()
                tstate._event_queue.pop(-1)

            __finalize_thread__()
            alive_lock.release()


        from ._internal import tstate as _ts
        _ts.name_thread_root_function(_inner)

        startsync_lock.acquire()
        tid = _thread.start_new_thread(_inner, ())
        startsync_lock.acquire()
        startsync_lock.release()
        res = ThreadActivity.__new__(ThreadActivity, tid)
        res._alive_lock = alive_lock
        return res

    @property
    def __wrapped__(self):
        return self._wrapped

    @property
    def __signature__(self):
        return self._signature


class ThreadActivity:
    _cache = {}

    __slots__ = (
        "_state",
        "_alive_lock",
    )

    def __new__(cls, *args, **kwargs):
        self = super().__new__(cls)
        if len(args) == 1:
            if isinstance(args[0], int):
                if args[0] in cls._cache:
                    return cls._cache[args[0]]
                self._state = TState(args[0])
                self._alive_lock = None
                cls._cache[args[0]] = self
                return self
            if isinstance(args[0], TState):
                if args[0].id in cls._cache:
                    return cls._cache[args[0].id]
                self._state = args[0]
                self._alive_lock = None
                cls._cache[args[0].id] = self
                return self

        raise TypeError("Illegal call to ThreadActivity.__new__.")

    def __init__(self, *args, **kwargs):
        raise TypeError("Illegal call to ThreadActivity.__init__.")

    def invoke(self, func: invokable, *args, **kwargs) -> ScheduledResult:
        """
        Schedule the thread to call the specified function given
        the specified arguments.
        This interrupts the thread as soon as possible to make it do
        the call. The call may not occur immediately, especially if the
        thread is inside a blocking function such as time.sleep.
        Also note that calls are executed in the order in which they were
        registered / invoked.
        Returns a ScheduledResult object which will be filled in with the
        result of the call when it returns.
        """
        return self._state.invoke(func.__wrapped__, *args, **kwargs)

    def join(self):
        """
        Wait until the thread terminates.
        """
        if self._alive_lock:
            self._alive_lock.acquire()
            self._alive_lock.release()
            return
        while self._state.alive():
            pass

    @property
    def tstate(self) -> TState:
        return self._state

    @property
    def alive(self) -> bool:
        if self._alive_lock:
            return self._alive_lock.locked()
        return self._state.alive()

    @classmethod
    @property
    def current_thread(cls):
        return cls.__new__(cls, TState.current())


def thread(func: _ThreadTarget):
    return ThreadDefinition(func)

