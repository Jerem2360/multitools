

class MyWeakRef:
    """
    Weak ref supporting any type of object
    """
    class _Inner:
        def __init__(self, obj: object):
            self._obj = obj

        def __eq__(self, other):
            if isinstance(other, MyWeakRef._Inner):
                return id(self._obj) == id(other._obj)
            return id(self._obj) == id(other)

        @property
        def obj(self):
            return self._obj

    def __init__(self, target):
        import weakref
        self._ref = weakref.ref(type(self)._Inner(target))
        self._strong = None

    def __eq__(self, other):
        if isinstance(other, MyWeakRef):
            return self._ref() == other._ref()
        return self._ref() == other

    def __call__(self, *args, **kwargs):
        if self._ref() is None:
            return None
        return self._ref().obj


class FrameKeeper:
    def __init__(self, obj):
        if obj is None:
            raise TypeError("None cannot be held.")
        import weakref
        self._ref = MyWeakRef(obj)
        self._strongref = None

    def __enter__(self):
        self._strongref = self._ref()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._strongref = None


class FrameEmulator:
    from .secretattr import prefix

    frame_attr_name = prefix + ''

    def __new__(cls, frame, *args, **kwargs):
        if cls.frame_attr_name in frame.f_locals:
            return frame.f_locals[cls.frame_attr_name]

        self = super().__new__(cls)
        self._initialized = False
        frame.f_locals[cls.frame_attr_name] = self
        return self

    def __init__(self, frame, trace=None, trace_opcodes=None, trace_lines=None):
        if self._initialized:
            return
        import types
        if not isinstance(frame, types.FrameType):
            raise TypeError("FrameEmulator must refer to an existing frame.")
        if not (callable(trace) or trace is None):
            raise TypeError("Frame trace function must be callable or None.")
        if not isinstance(trace_opcodes, (bool, type(None))):
            raise TypeError("Frame.f_trace_opcodes must be bool.")
        if not isinstance(trace_lines, (bool, type(None))):
            raise TypeError("Frame.f_trace_lines must be bool.")

        self._id = id(frame)
        self._ref = MyWeakRef(frame)
        self._trace = trace if callable(trace) else frame.f_trace
        self._trace_opcodes = trace_opcodes if isinstance(trace_opcodes, bool) else frame.f_trace_opcodes
        self._trace_lines = trace_lines if isinstance(trace_lines, bool) else frame.f_trace_lines

        self._initialized = True

    # properties and methods to actually emulate the frame:
    def hold(self):
        """
        Enter a context during which the frame is guaranteed to stay alive.
        """
        return FrameKeeper(self._ref())

    def __getattr__(self, item):
        return getattr(self._ref(), item)

    @property
    def f_trace(self):
        return self._trace

    @f_trace.setter
    def f_trace(self, value):
        if not (callable(value) or value is None):
            raise TypeError("Frame.f_trace must be callable or None.")
        self._trace = value

    @property
    def f_trace_opcodes(self):
        return self._trace_opcodes

    @f_trace_opcodes.setter
    def f_trace_opcodes(self, value):
        if not isinstance(value, bool):
            raise TypeError("Frame.f_trace_opcodes must be bool.")
        self._trace_opcodes = value

    @property
    def f_trace_lines(self):
        return self._trace_lines

    @f_trace_lines.setter
    def f_trace_lines(self, value):
        if not isinstance(value, bool):
            raise TypeError("Frame.f_trace_lines must be bool.")
        self._trace_lines = value

    # properties to manage the emulator:
    @property
    def id(self):
        return self._id

    @property
    def alive(self):
        return self._ref() is not None

    @property
    def referee(self):
        if self._ref is None:
            return
        if not self.alive:
            self._ref = None
            return
        return self._ref()

    @referee.setter
    def referee(self, value):
        import types
        if not isinstance(value, types.FrameType):
            raise TypeError("referee value must be a frame.")
        self._ref = MyWeakRef(value)


class TState:
    """
    Internal class representing the status of a python thread.
    This type can only have one instance per running thread.
    """
    _cache = {}

    def __new__(cls, tid, *args, **kwargs):
        if tid in cls._cache:
            return cls._cache[tid]
        self = super().__new__(cls)
        self._initialized = False
        cls._cache[tid] = self
        return self

    def __init__(self, tid, frame):
        import sys
        from .event_loop import EventLoop
        if self._initialized:
            return

        if tid not in sys._current_frames():
            raise ValueError(f"Unknown thread with id {hex(tid)}.")

        self._id = tid
        self._current_frame = FrameEmulator(frame)
        self._first_frame = None
        self._event_loop = EventLoop()
        self._traces = {
            '*': [],
            'call': [],
            'line': [],
            'return': [],
            'exception': [],
            'opcode': [],
        }

        self._initialized = True

    def __trace__(self, frame, event, arg):
        def call_trace(t, *args):
            import sys
            try:
                need_remove = t(*args)
            except SystemExit:
                raise
            except BaseException as e:
                print(f"Exception ignored in trace function '{t}':", file=sys.stderr)
                sys.excepthook(type(e), e, e.__traceback__)
                return False
            return not need_remove

        to_pop = []
        for trace in self._traces['*']:
            if not call_trace(trace, frame, event, arg):
                to_pop.append(trace)

        for _t in to_pop:
            self._traces['*'].pop(self._traces['*'].index(_t))

        to_pop.clear()
        for trace in self._traces.get(event, []):
            if not call_trace(trace, frame, arg):
                to_pop.append(trace)

        for _t in to_pop:
            self._traces[event].pop(self._traces[event].index(_t))


    def __event__(self):
        """
        Called from the thread when it should try to call one of
        its events.
        """
        return self._event_loop.run_event()

    def __leave__(self):
        """
        Called just before the thread exits and multitools is active.
        """
        import _thread
        # empty the event queue by calling each remaining event one by one before the thread exits
        while self.__event__():
            pass

        # remove ourselves from the cache as the thread is about to exit
        try:
            del type(self)._cache[_thread.get_ident()]
        except:
            pass
        del self._first_frame
        print('leaving')

    @classmethod
    def current(cls):
        import _thread
        import sys
        return cls(_thread.get_ident(), sys._getframe(1))

    @classmethod
    def from_id(cls, tid):
        import sys
        return cls(tid, sys._current_frames()[tid])

    def __prepare_frames__(self):
        """
        Prepare this thread's frames for when all frames
        in the interpreter are wrapped.
        """
        import sys
        top_frame = sys._current_frames().get(self._id, None)

        if top_frame is None:
            return False

        frame = top_frame

        while True:
            FrameEmulator(frame)  # save the state (mainly f_trace) of the frame
            if frame.f_back is None:
                self._first_frame = frame  # keep track of the first frame of the thread
                break
            frame = frame.f_back

        return True

    def __wrap_frames__(self, common_trace):
        """
        Initialize all the threads' currently active frames with the
        specified common trace function.
        """
        import sys
        frame = sys._current_frames().get(self._id, None)
        if frame is None:
            return False

        while 1:
            frame.f_trace = common_trace
            frame.f_trace_opcodes = True

            if frame.f_back is None:
                break
            frame = frame.f_back

        return True

    def __restore__(self):
        """
        Restore the thread's frames as they would have been without multitools.
        """
        import sys

        frame = sys._current_frames().get(self._id, None)
        if frame is None:
            return False

        while True:
            em = FrameEmulator(frame)

            frame.f_trace = em.f_trace
            frame.f_trace_opcodes = em.f_trace_opcodes
            frame.f_trace_lines = em.f_trace_lines

            try:
                del frame.f_locals[FrameEmulator.frame_attr_name]
            except:
                pass

            if frame.f_back is None:
                break

            frame = frame.f_back

        return True

    def is_leaving(self, frame, event):
        if event != 'return':
            return False

        if isinstance(frame, FrameEmulator):
            return frame.id == id(self._first_frame)

        return id(frame) == id(self._first_frame)

    def schedule_invoke(self, func, *args, **kwargs):
        """
        Schedule the specified function or callable to be
        called with the specified arguments in the thread.
        Scheduled tasks might not be run immediately.
        """
        import inspect
        if not callable(func):
            raise TypeError("func must be callable.")

        try:
            sig = inspect.signature(func)
            sig.bind(*args, **kwargs)
        except TypeError:
            raise TypeError("Arguments are incompatible with function signature.")

        return self._event_loop.schedule_invoke(func, *args, **kwargs)

    def schedule_exception(self, exc):
        """
        Schedule the specified exception to be raised in the thread.
        Note that when a thread exits with an exception, the remaining
        scheduled events are not dispatched.
        """
        if isinstance(exc, type) and issubclass(exc, Exception):
            self._event_loop.schedule_exception(exc())
            return

        if isinstance(exc, Exception):
            self._event_loop.schedule_exception(exc)
            return

        raise TypeError("exc must be an Exception.")

    def schedule_exit(self, code=0):
        """
        Schedule the thread to exit as fast as possible.
        Note that this bypasses the call of all events
        scheduled after this one.
        """
        if hasattr(code, '__index__'):
            code = code.__index__()

        if not isinstance(code, int):
            raise TypeError("code must be an integer.")

        self._event_loop.schedule_exit(code)

    def schedule_keyboard_interrupt(self):
        self._event_loop.schedule_keyboard_interrupt()

    def addtrace(self, func, event='*', /):
        """
        Add a tracing function for the thread.
        The specified function must take (frame, event, arg)
        as parameters.
        If event is specified, the tracing function
        will only be called for that specific event,
        and it must take (frame, arg) as parameters.
        See sys.settrace for possible values of event.
        """
        if not callable(func):
            raise TypeError("func must be callable.")
        if event not in self._traces:
            raise ValueError("event must be one of", ', '.join(self._traces.keys()) + '.')
        self._traces[event].append(func)

