
"""
Private api to python's runtime state
"""
import sys
from .asynctools import AsyncMap
from types import TracebackType


SUPPORT_SIGNALS = True
try:
    import signal as _sgn
except ImportError:
    SUPPORT_SIGNALS = False


def __thread_begin__():
    """
    Called at the beginning of the lifetime of each new thread.
    """
    import threading as _thr
    for th in _thr.enumerate():
        TState(tid=th.ident)
    del _thr



class ExcInfoProxy:
    __slots__ = (
        '_id',
    )

    def __init__(self, tid):
        self._id = tid

    def raw(self) -> tuple:
        """
        Raw exception information. Equivalent to calling sys.exc_info() in the thread.
        """
        return sys._current_exceptions().get(self._id, None)  # type: ignore

    @property
    def type(self) -> type[BaseException] | None:
        """
        The type of the exception being handled in the thread. This is None
        if no exception is being handled.
        """
        raw = self.raw()
        if raw is None:
            return
        return raw[0]

    @property
    def value(self) -> BaseException | None:
        """
        The exception object being handled in the thread. This is None
        if no exception is being handled.
        """
        raw = self.raw()
        if raw is None:
            return
        return raw[1]

    @property
    def traceback(self) -> TracebackType | None:
        """
        The optional traceback object of the exception being handled in
        the thread. This is None if undefined or no exception is being
        handled.

        """
        raw = self.raw()
        if raw is None:
            return
        return raw[2]

    def __repr__(self):
        return f"<exception state of thread {hex(self._id)}>"


class _CallStackIterator:
    __slots__ = (
        '_frame',
    )

    def __init__(self, start_frame):
        self._frame = start_frame

    def __next__(self):
        if self._frame is None:
            raise StopIteration
        res = self._frame
        self._frame = self._frame.f_back
        return res

    def __repr__(self):
        return f"<call stack iterator at {hex(id(self))}>"


class CallStackProxy:
    __slots__ = (
        '_id',
    )

    def __init__(self, tid):
        self._id = tid

    def __getitem__(self, item):

        if not isinstance(item, int):
            raise TypeError('item')

        current = sys._current_frames().get(self._id, None)  # type: ignore
        if current is None:
            return None

        if item < 0:
            x = -len(self)
            while True:
                if current is None:
                    break
                if x == item:
                    return current
                current = current.f_back
                x += 1

            return

        for i in range(item):
            if current is None:
                raise IndexError(f"Call stack for thread {hex(self._id)} is not deep enough")
            current = current.f_back

        return current

    def __len__(self):
        i = 0
        current = sys._current_frames().get(self._id, None)  # type: ignore

        while True:
            if current is None:
                return i
            current = current.f_back
            i += 1

    def __iter__(self):
        return _CallStackIterator(self[0])

    def __repr__(self):
        return f"<call stack of thread {hex(self._id)}>"


class _InvokeObject:
    __slots__ = (
        '_callable',
        '_args',
        '_thread'
    )

    def __init__(self, obj, arglist, kwdict={}):
        import _thread
        self._callable = obj
        self._args = arglist, kwdict
        self._thread = _thread.get_ident()

    def call(self):
        args, kwargs = self._args
        self._callable(*args, **kwargs)

    @property
    def callable(self):
        return self._callable

    @property
    def source(self):
        return self._thread

    def __repr__(self):
        return f"<invokable {repr(self._callable).removeprefix('<').removesuffix('>')}>"


class _InvokeQueueIterator:
    __slots__ = (
        '_index',
        '_queue',
    )

    def __init__(self, queue):
        self._index = 0
        self._queue = queue

    def __next__(self):
        if self._index >= len(self._queue):
            raise StopIteration
        res = self._queue[self._index]
        self._index += 1
        return res

    def __repr__(self):
        return f"<invoke queue iterator at {hex(id(self))}>"


class InvokeQueueProxy:
    """
    Invoke queue associated with a specific thread.
    Functions are invoked in register order.
    """
    __slots__ = (
        '_id',
    )

    def __init__(self, tid):
        self._id = tid

    def __getitem__(self, item):
        return TState._objects[self._id]._invoke_queue[item].callable

    def __len__(self):
        return len(TState._objects[self._id]._invoke_queue)

    def push(self, obj, arglist=(), kwdict={}):
        """
        Push a function at the end of the invoke queue.
        """
        TState._objects[self._id]._invoke_queue.append(_InvokeObject(obj, arglist, kwdict))

    def pop(self):
        """
        Remove and return the function at the end of the invoke queue.
        If the queue is empty, do nothing and return None.
        """
        if not len(TState._objects[self._id]._invoke_queue):
            return None
        return TState._objects[self._id]._invoke_queue.pop(-1)

    def __iter__(self):
        return _InvokeQueueIterator(TState._objects[self._id]._invoke_queue)

    def __repr__(self):
        return f"<invoke queue of thread {hex(self._id)}>"


class TState:
    _objects = AsyncMap()

    if SUPPORT_SIGNALS:
        __slots__ = (
            '_id',
            '_lock',
            '_invoke_queue',
            '_tracing_functions',
            '_need_exit',
            '_exit_code',
        )
    else:
        __slots__ = (
            '_id',
            '_lock',
            '_invoke_queue',
            '_tracing_functions',
            '_signals',
            '_exit_code',
        )

    def __new__(cls, *args, **kwargs):  # needs an update depending on SUPPORTS_SIGNALS
        import _thread
        tid = kwargs.get('tid', _thread.get_ident())
        if tid in cls._objects:
            return cls._objects[tid]
        self = super().__new__(cls)
        self._id = tid
        self._lock = _thread.allocate_lock()
        self._invoke_queue = []
        self._need_exit = False
        self._exit_code = 0
        self._tracing_functions = {
            'call': [],
            'line': [],
            'return': [],
            'exception': [],
            'opcode': [],
        }
        for frame in self.call_stack:
            frame.f_trace = self.__trace__
            frame.f_trace_opcodes = True
        sys.settrace(self.__trace__)
        cls._objects[tid] = self
        return self

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __trace__(self, frame, event, args):
        if SUPPORT_SIGNALS:
            if sys.is_finalizing():  # stop tracing if shutting down
                self.__finalize__(frame)
            from . import errors
            for trace in self._tracing_functions[event]:
                with errors.frame_mask():
                    trace(frame, args)
            if len(self._invoke_queue):
                invoke = self._invoke_queue.pop(0)
                with errors.frame_mask():
                    try:
                        invoke.expand()
                    except SystemExit:
                        raise
                    except:
                        print(f"Exception raised in function '{invoke.callable.__qualname__}' invoked by thread '{hex(invoke.source)}' in thread '{hex(self._id)}'.", file=sys.stderr)
                        sys.excepthook(*sys.exc_info())

            if self._need_exit:  # catch an eventual terminating signal, and exit the thread as fast as possible.
                self._need_exit = False
                sys.exit(self._exit_code)
            return self.__trace__

        try:
            if sys.is_finalizing():  # stop tracing if shutting down
                self.__finalize__(frame)
            from . import errors
            for trace in self._tracing_functions[event]:
                with errors.frame_mask():
                    trace(frame, args)
            if len(self._invoke_queue):
                invoke = self._invoke_queue.pop(0)
                with errors.frame_mask():
                    try:
                        invoke.expand()
                    except SystemExit:
                        raise
                    except:
                        print(
                            f"Exception raised in function '{invoke.callable.__qualname__}' invoked by thread '{hex(invoke.source)}' in thread '{hex(self._id)}'.",
                            file=sys.stderr)
                        sys.excepthook(*sys.exc_info())

            if self._need_exit:  # catch an eventual terminating signal, and exit the thread as fast as possible.
                self._need_exit = False
                sys.exit(self._exit_code)
            return self.__trace__
        except KeyboardInterrupt:
            import signal  # no, signal is not supported in this case.


    def __finalize__(self, frame):
        try:
            frame.f_trace = None
            del type(self)._objects[self._id]
        except:
            pass

    def trace(self, event):
        """
        Decorator to register a tracing function for the specified event.
        Event '*' means every possible event.
        """
        def inner(fn):
            self._tracing_functions[event].append(fn)
            return fn
        return inner

    def exit(self, code):
        """
        Tell the thread to exit as fast as possible.
        This can only interrupt python code. Finalizers
        are executed and runtime terminates properly.
        """
        self._exit_code = code
        if sys.is_finalizing():
            return
        self._need_exit = True

    @property
    def exiting(self):
        """
        Return if the thread is exiting.
        """
        return self._need_exit or sys.is_finalizing()

    @classmethod
    def _threading_trace(cls, frame, event, args):
        import threading
        print('here', threading.get_ident())
        state = cls.current()
        if sys.gettrace() != state.__trace__:
            sys.settrace(state.__trace__)
        return state.__trace__

    @classmethod
    def current(cls) -> 'TState | None':
        import _thread
        return cls._objects.get(_thread.get_ident(), None)

    @property
    def id(self):
        if self._id not in sys._current_frames():
            return 0
        return self._id

    @property
    def exc_info(self):
        return ExcInfoProxy(self._id)

    @property
    def call_stack(self):
        return CallStackProxy(self._id)

    @property
    def invoke_queue(self):
        return InvokeQueueProxy(self._id)

    def __repr__(self):
        return f"<TState for thread {hex(self._id)}>"


def __thread_terminate__():
    """
    Called at the end of each thread's lifetime.
    """
    from . import errors
    state = TState.current()
    for invoke in state.invoke_queue:
        with errors.frame_mask():
            try:
                invoke.expand()
            except SystemExit:
                return
            except:
                print(f"Exception raised in function '{invoke.callable.__qualname__}' invoked by thread '{hex(invoke.source)}' in thread '{hex(state.id)}'.", file=sys.stderr)
                sys.excepthook(*sys.exc_info())

