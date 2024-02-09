"""
Code that allows multitools to add support for custom events to the python runtime.
These functions should not be used instead of the "public" ones available outside
the '_internal' package as the formers are undocumented and using them in the wrong
way may break python itself.
"""


class FrameEmulation:
    _frames = {}

    def __new__(cls, frame, *args, **kwargs):
        if id(frame) in cls._frames:
            return cls._frames[id(frame)]
        self = super().__new__(cls)
        cls._frames[id(frame)] = self
        self._initialized = False
        return self

    def __init__(self, frame):
        if self._initialized:
            return
        self._frame = frame
        self._f_trace_opcodes = frame.f_trace_opcodes
        self._f_trace_lines = frame.f_trace_lines

    def __getattr__(self, item):
        return getattr(self._frame, item)

    @property
    def f_trace_opcodes(self):
        return self._f_trace_opcodes

    @f_trace_opcodes.setter
    def f_trace_opcodes(self, value):
        if not isinstance(value, bool):
            raise TypeError("attribute value must be bool.")
        self._f_trace_opcodes = value

    @property
    def f_trace_lines(self):
        return self._f_trace_lines

    @f_trace_lines.setter
    def f_trace_lines(self, value):
        if not isinstance(value, bool):
            raise TypeError("attribute value must be bool.")
        self._f_trace_lines = value


class _ExecutionLoop:
    __slots__ = (
        '_wrapped',
        '_initialized',
        '_initialized_for_threads',
        '__weakref__',
    )

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
        secretattr.setattr(sys.modules[cls.__module__], 'ExecLoop_cache', self)
        return self

    def _init_trace(self, frame, event, arg):
        pass

    def __init__(self):
        if self._initialized:
            return

        self._initialized = True

    def __init_thread__(self, tid):
        pass

    def __finalize_thread__(self, tid):
        pass

    def __del__(self):
        if not self._initialized:
            return

        self._initialized = False


class ExecutionLoop:
    __wrapped__ = {}
    _initialized_for_threads = {}
    _initialized = False

    @classmethod
    def _run_events(cls, frame, event, arg):
        pass

    @classmethod
    def __wrap__(cls, frame, event, arg):
        import _thread
        wrapped = cls.__wrapped__.get(_thread.get_ident(), None)
        if not wrapped:
            return

        if event == 'opcode' and not FrameEmulation(frame).f_trace_opcodes:
            return
        if event == 'line' and not FrameEmulation(frame).f_trace_lines:
            return

        cls.__wrapped__[_thread.get_ident()] = wrapped(FrameEmulation(frame), event, arg)

    @classmethod
    def __loop__(cls, frame, event, arg):
        """
        This function is called each iteration of python's execution loop.
        It allows this library to make the python runtime look and behave
        like an event loop.
        """
        if not frame.f_trace_opcodes:
            frame.f_trace_opcodes = True

        cls.__wrap__(frame, event, arg)

        cls._run_events(frame, event, arg)

        if event == 'return' and id(frame) in FrameEmulation._frames:
            del FrameEmulation._frames[id(frame)]
            print('deleted')

        return cls.__loop__

    @classmethod
    def __initialize__(cls):
        """
        Initialize global event loop status.
        """
        if cls._initialized:
            return

        import weakref
        import sys

        split = cls.__module__.rsplit('.', 3)
        if not len(split):
            raise RuntimeError("The multitools module was not imported correctly.")
        multitools = sys.modules.get(split[0], None)
        if not multitools:
            raise RuntimeError("The multitools module was not imported correctly.")
        weakref.finalize()


        for tid in sys._current_frames().keys():
            cls.__initialize_thread__(tid)

        from . import function_reassigner
        function_reassigner.reassign(sys.settrace, function_reassigner._settrace)
        function_reassigner.reassign(sys.gettrace, function_reassigner._gettrace)

        cls._initialized = True

    @classmethod
    def __initialize_thread__(cls, tid):
        """
        Initialize event loop status for the specified thread.
        """
        if cls._initialized_for_threads.get(tid, False):
            return  # prevent this function from being called twice for the same thread

        import sys
        if tid not in sys._current_frames().keys():
            import warnings
            warnings.warn("Tried to initialize a thread that does not exist. This is most likely an error or a bug.", RuntimeWarning)
            return

        old_trace = sys.gettrace()
        sys.settrace(cls.__loop__)
        frame = sys._current_frames().get(tid, None)

        while True:
            # we don't care about tracing the current frame as it will be destroyed once this
            # function returns (and it would actually create infinite recursion, by the way)
            if frame.f_back is None:
                break
            frame = frame.f_back
            frame.f_trace = cls.__loop__
            frame.f_trace_opcodes = True

        from . import function_reassigner

        if old_trace:
            function_reassigner._settrace(sys.settrace, old_trace)
        cls._initialized_for_threads[tid] = True

    @classmethod
    def __finalize__(cls):
        """
        Finalize global event loop status.
        """
        import sys
        from . import function_reassigner

        if not cls._initialized:
            return

        for tid in sys._current_frames().keys():
            cls.__finalize_thread__(tid)

        sys.setswitchinterval = function_reassigner.__sys_setswitchinterval__
        sys.setrecursionlimit = function_reassigner.__sys_setrecursionlimit__
        sys.settrace = function_reassigner.__sys_settrace__
        sys.gettrace = function_reassigner.__sys_gettrace__

        cls._initialized = False

    @classmethod
    def __finalize_thread__(cls, tid):
        """
        Finalize event loop status for the specified thread.
        """
        import warnings
        if not cls._initialized_for_threads.get(tid, False):
            warnings.warn("Tried to finalize an unknown thread from the multitools library. This is most likely an error or a bug.", RuntimeWarning)
            return

        import sys
        if tid not in sys._current_frames().keys():
            return

        cls._initialized_for_threads[tid] = False



