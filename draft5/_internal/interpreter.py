

class InterpreterState:
    def __init__(self):
        raise TypeError("Abstract class.")

    @classmethod
    def create_interpreter(cls):
        """
        Create a new sub-interpreter inside the current environment.
        """
        import _xxsubinterpreters
        iid = _xxsubinterpreters.create()
        return SubInterpreterState(iid)

    @classmethod
    def current(cls) -> 'InterpreterState':
        """
        Return the state of the currently running interpreter.
        """
        import _xxsubinterpreters
        iid = _xxsubinterpreters.get_current()
        if iid == _xxsubinterpreters.get_main():
            return MainInterpreterState()
        return SubInterpreterState(iid)

    @classmethod
    def main(cls) -> 'InterpreterState':
        return MainInterpreterState()

    def run_string(self, script, shared) -> bool: ...

    def destroy(self): ...

    @property
    def id(self) -> int: ...

    @property
    def running(self) -> bool: ...

    @classmethod
    @property
    def shareable(cls, obj) -> bool:
        import _xxsubinterpreters
        return _xxsubinterpreters.is_shareable(obj)


class SubInterpreterState(InterpreterState):
    _cache = {}

    def __new__(cls, iid=0, *args, **kwargs):
        if iid in cls._cache:
            return cls._cache[iid]

        self = super().__new__(cls)
        self._initialized = False
        cls._cache[iid] = self
        return self

    def __init__(self, iid):
        if self._initialized:
            return
        self._id = iid
        self._initialized = True

    def run_string(self, script, shared) -> bool:
        import _xxsubinterpreters
        return not _xxsubinterpreters.run_string(self._id, script, shared)

    def destroy(self):
        import _xxsubinterpreters
        _xxsubinterpreters.destroy(self._id)
        del type(self)._cache[self._id]

    @property
    def id(self):
        return self._id

    @property
    def running(self) -> bool:
        import _xxsubinterpreters
        return _xxsubinterpreters.is_running(self._id)


class MainInterpreterState(InterpreterState):
    _cache = None

    def __new__(cls, *args, **kwargs):
        import weakref
        import sys
        from . import secretattr
        if (cls._cache is not None) and (cls._cache() is not None):
            return cls._cache()

        self = super().__new__(cls)
        self._initialized = False
        cls._cache = weakref.ref(self)
        secretattr.setattr(sys.modules[cls.__module__], 'MainInterpState', self)
        return self

    def __init__(self):
        if self._initialized:
            return
        import sys
        import _xxsubinterpreters
        from . import tstate

        self._threads = {}

        # prepare frames by storing their previous traces in their respective emulators
        for tid, top_frame in sys._current_frames().items():
            state = tstate.TState(tid, top_frame)
            state.__prepare_frames__()
            self._threads[tid] = state

        self._iid = _xxsubinterpreters.get_main()

        # set up our trace function inside all threads
        sys._settraceallthreads(self._trace)

        # initialize all frames with our custom function
        for tid, tstate in self._threads.items():
            tstate.__wrap_frames__(self._trace)

        """
        At this point, all threads have received our trace function and have it
        wrapping the one that was previously in place.
        """

        self._initialized = True

    def _trace(self, frame, event, arg):
        from .tstate import FrameEmulator, TState

        # call the wrapped trace function using the frame emulation.
        frame_emulation = FrameEmulator(frame)
        if frame_emulation.f_trace == self._trace:
            frame_emulation.f_trace = None

        if callable(frame_emulation.f_trace):
            res = frame_emulation.f_trace(frame_emulation, event, arg)
            if event == 'call':  # the passed in frame is the entered frame
                frame_emulation.f_trace = res

        tstate = TState.current()
        # call the current thread's events
        tstate.__event__()

        # call the current thread's tracing functions
        tstate.__trace__(frame_emulation, event, arg)

        # cleanup the TState if the thread is about to terminate
        if tstate.is_leaving(frame, event):
            tstate.__leave__()

        return self._trace

    def __del__(self):
        try:
            import sys
        except ImportError:  # can occur if python is finalizing e.g. in destructors
            return
        if sys is None or sys.is_finalizing():
            return
        for state in self._threads.values():
            state.__restore__()  # restore the frame traces before removing their emulators

    def run_string(self, script, shared) -> bool:
        if not isinstance(shared, dict):
            raise TypeError("shared must be a dictionary mapping names to values.")
        for key in shared.keys():
            if not isinstance(key, str):
                raise TypeError("shared must be a dictionary mapping names to values.")

        import _xxsubinterpreters
        return not _xxsubinterpreters.run_string(self._iid, script, shared)

    def destroy(self):
        raise RuntimeError("Cannot destroy the main interpreter.")

    @classmethod
    @property
    def _subinterpreters(cls):
        return tuple(SubInterpreterState._cache.values())

    @property
    def id(self) -> int:
        return self._iid

    @property
    def running(self) -> bool:
        import _xxsubinterpreters
        return _xxsubinterpreters.is_running(self._iid)

