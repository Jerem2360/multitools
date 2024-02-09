from typing import Callable

from .protocols import WrapsExcInfo, WrapsCallStack


def notify(tstate):
    import sys

    if tstate._id not in sys._current_frames():
        del TState._cache[tstate._id]


def _get_caller_file(frame=None):
    if frame is None:
        frame = TState.current().call_stack[2]
    else:
        frame = frame.f_back
    return frame.f_code.co_filename


def make_tracefunc(ts, tracefunc):
    # print("making trace function", tracefunc)
    import sys
    for frame in ts.call_stack:
        if frame.f_code.co_filename.startswith("<frozen "):
            continue
        frame.f_trace = tracefunc
    sys.settrace(tracefunc)


def mask_frame(tstate, frame):
    if frame not in tstate._masked_frames:
        tstate._masked_frames.append(frame)


def unmask_frame(tstate, frame):
    import sys
    # print("debug", frame, sys._getframe(1))
    if frame in tstate._masked_frames:
        tstate._masked_frames.pop(tstate._masked_frames.index(frame))


def mask_frames_from_now(tstate):
    tstate._mask_frame = True


def unmask_frames_from_now(tstate):
    tstate._mask_frame = False


def are_frames_masked(tstate):
    return tstate._mask_frame


def name_thread_root_function(function):
    function.__qualname__ = function.__qualname__.replace(function.__name__, "<thread>")
    function.__name__ = "<thread>"
    function.__code__ = function.__code__.replace(co_name="<thread>")
    return function


def check_threadfunc_valid_signature(func: Callable[..., ...]):
    import inspect
    sig = inspect.signature(func)
    if hasattr(func, '__qualname__'):
        img = func.__qualname__ + str(sig)
    else:
        img = repr(func) + str(sig)
    if not len(sig.parameters):
        raise TypeError(f"Invalid function signature '{img}'. Thread functions must at least accept one positional argument.")
    firstparam = tuple(sig.parameters.values())[0]
    if firstparam.kind in (inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.VAR_KEYWORD):
        raise TypeError(f"Invalid function signature '{img}'. Thread functions must at least accept one positional argument.")


def get_threadfunc_signature(func: Callable[..., ...]):
    import inspect
    full_sig = inspect.signature(func)
    full_params = full_sig.parameters
    treated_params = []
    for i in range(len(full_params)):
        param = list(full_params.values())[i]
        if i > 0 or param.kind == inspect.Parameter.VAR_POSITIONAL:
            treated_params.append(param)
    return full_sig.replace(parameters=treated_params)



class StopTracing(BaseException):
    """
    Tells the tracing machinery to not trace more recently registered tracing functions.
    In other words, this causes the tracing machinery to break out of the tracing loop.
    """
    pass


class TState:
    __slots__ = (
        '_id',
        '_init',
        '_traces',
        '_tracing',
        '_event_queue',
        '_mask_frame',
        '_masked_frames',
        '_propagating_exception',
        '_counter',
        '_do_trace',
        '_do_events',
    )

    _cache = {}

    def __new__(cls, tid, *args, **kwargs):
        import sys
        if tid in cls._cache:
            return cls._cache[tid]
        if tid not in sys._current_frames():
            raise TypeError(f"Can't find thread '{tid}'")
        self = super().__new__(cls)
        self._id = 0
        self._init = False
        cls._cache[tid] = self
        return self

    def __init__(self, tid, *args, **kwargs):
        if self._init:
            return
        self._id = tid
        self._traces = {
            'call': [],
            'line': [],
            'exception': [],
            'return': [],
            'opcode': [],
            '*': []
        }
        self._tracing = False
        self._event_queue = []
        self._mask_frame = False
        self._masked_frames = []
        self._propagating_exception = None
        self._counter = 0
        self._do_trace = False
        self._do_events = False

        self._init = True

    @classmethod
    def current(cls):
        """
        Return the state of the current thread.
        """
        import _thread
        return cls(_thread.get_ident())

    @classmethod
    def trace_break(cls):
        """
        Do not call the current trace and more recently registered
        functions while tracing.
        Never returns to the caller.
        Does nothing if called outside a tracing function call.
        """
        tstate = TState.current()
        if tstate._tracing:
            raise StopTracing

    def add_trace(self, trace, *, event='*'):
        """
        Register a tracing function for the thread. Tracing functions
        are called in register order.
        'event' specifies which event the tracing function should target.
        It defaults to all events ('*').

        If targeting a specific event, the function must take 2 parameters:
        tstate and arg.
        If targeting all events, the function must take 3 parameters:
        tstate, event and arg.
        If a tracing function raises an exception, it is unregistered.
        """
        self._traces[event].append(trace)

    def invoke(self, func, *args, **kwargs):
        """
        Schedule the thread to run the specified function with the specified arguments
        before continuing its normal activity. Any invokes scheduled after the thread
        has raised an exception will not be called.

        When a thread terminates without an exception, all remaining invokes are called.

        Invoking a function that never returns in a thread will cause that thread to never
        terminate, eventually not running part of its code.
        Exceptions raised inside invokes are handled correctly, and a call to sys.exit() will
        kill the thread.
        Invoking in the current thread does the same as calling the specified function normally.

        Return a ScheduledResult object which will be set when the function returns.
        """
        from . import runtime
        import _thread
        if self._id == _thread.get_ident():
            event = runtime.ThreadEvent.new_invoke(func, args, kwargs)
            if event.run():
                raise SystemExit(1)
            return event.result
        event = runtime.ThreadEvent.new_invoke(func, args, kwargs)
        self._event_queue.insert(0, event)
        return event.result

    def throw(self, exc):
        """
        Schedule an exception to be raised in the thread.
        """
        from . import runtime
        self._event_queue.append(runtime.ThreadEvent.new_throw(exc))

    def exit(self, code=0, /):
        """
        Schedule the thread to exit. May not occur immediately.
        """
        self.throw(SystemExit(code))

    @property
    def call_stack(self) -> WrapsCallStack:
        """
        The current thread's call stack as an iterable of Frame objects.
        """
        from . import runtime
        return runtime.CallStackProxy(self._id)

    @property
    def exc_info(self) -> WrapsExcInfo:
        """
        The current thread's exception status.
        """
        from . import runtime
        return runtime.ExcInfoProxy(self._id)

    @property
    def id(self):
        return self._id

    @property
    def alive(self):
        """
        Return whether the thread is alive, a.k.a. if it is still executing python code.
        TState objects may be reused for another thread once it has terminated.
        """
        import sys
        return self._id in sys._current_frames()

    def __repr__(self):
        return f"<TState for thread {self._id}>"

