import types

DEFAULT_SWITCH_INTERVAL = 0.005

"""
Provides a low-level view on thread, interpreter and global status.
"""


class SecurityCriticalProperty:
    """
    Class that helps avoid race conditions while serving
    as a proxy buffer. Doesn't have any knowledge
    of the actual proxied object. Must be updated each time
    the value of the proxied object changes.
    """
    def __init__(self, initial_value):
        import _thread
        self._value = initial_value
        self._changed = False
        self._lock = _thread.allocate_lock()

    def acquire(self):
        # typical update scheme is:
        # if prop.acquire():
        #     prop.update(...)
        #     prop.release()
        return self._lock.acquire()

    def release(self):
        if self._lock.locked():
            self._lock.release()

    def update(self, new_value):
        if not self._lock.locked():
            raise RuntimeError(
                "Tried to update a security-critical property in an non-threadsafe manner. Make sure the \n"
                "property is acquired before doing this."
            )
        self._value = new_value
        print('update:', new_value)

    @property
    def value(self):
        with self._lock:
            return self._value

    @value.setter
    def value(self, value):
        with self._lock:
            self._value = value
            self._changed = True

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return self.value

    def __set__(self, instance, value):
        self.value = value


class ThreadStatus:
    """
    This describes properties of the interpreter and this library
    that are unique to each thread.
    """

    threads = {}

    def __init__(self, tid):
        self.trace_functions = {
            'call': [],
            'line': [],
            'exception': [],
            'return': [],
            'opcode': [],
            '*': []
        }
        self.id = tid
        self.event_queue = []
        self.is_tracing = False
        self.calls_events = False

    @property
    def current_frame(self):
        import sys
        return sys._current_frames().get(self.id, 0)

    def __trace__(self, frame, event, arg):
        frame.f_trace_opcodes = True
        return self.__trace__

class InterpreterStatus:
    """
    This describes properties of the interpreter and this library
    that are unique to each sub-interpreter.
    """

    interpreters = {}

    def __init__(self, iid):  # iid should be obtained using module '_xxsubinterpreters'
        import sys
        self.id = iid
        self.current_thread = None

        self.switch_interval = SecurityCriticalProperty(DEFAULT_SWITCH_INTERVAL)
        self.recursion_limit = SecurityCriticalProperty(sys.getrecursionlimit())

    def validate(self):
        import _xxsubinterpreters
        return self.id in _xxsubinterpreters.list_all()

    def __serialize__(self, pipe_reader):
        import pickle
        return pickle.dumps({
            'id': self.id,
            'SI': self.switch_interval.value,
            'RL': self.recursion_limit.value,
            'pipe': pipe_reader,
        })

    @classmethod
    def __deserialize__(cls, data):
        import pickle
        mapping = pickle.loads(data)
        self = cls(mapping['id'])
        self.switch_interval.value = mapping['SI']
        self.recursion_limit.value = mapping['RL']
        return self


class GlobalStatus:
    """
    This describes properties of the interpreter and this library
    that are shared between all threads and all sub-interpreters.
    """
    def __init__(self):
        pass

    @property
    def main_interpreter(self):
        import _xxsubinterpreters
        return InterpreterStatus(_xxsubinterpreters.get_main())

    @property
    def current_interpreter(self):
        import _xxsubinterpreters
        return InterpreterStatus(_xxsubinterpreters.get_current())

    @property
    def interpreters(self):
        import _xxsubinterpreters
        return list(InterpreterStatus(interpreter) for interpreter in _xxsubinterpreters.list_all())


def _serialize_function(func: types.FunctionType):
    import marshal
    import pickle
    data = {
        'CO': marshal.dumps(func.__code__),
        'M': func.__module__,
        'Q': func.__qualname__,
        'N': func.__name__,
        'A': func.__annotations__,
        'CL': None if func.__closure__ is None else tuple(cell.cell_contents for cell in func.__closure__),
        'DE': func.__defaults__,
        'K': func.__kwdefaults__,
        'DO': func.__doc__,
    }
    return pickle.dumps(data)


def _deserialize_function(serialized: bytes, _globals):
    import pickle
    import marshal
    import types

    data = pickle.loads(serialized)

    defaults = () if data['DE'] is None else data['DE']
    defaults += (() if data['K'] is None else data['K'])

    func = types.FunctionType(
        marshal.loads(data['CO']),
        _globals,
        data['N'],
        None if not len(defaults) else defaults,
        None if data['CL'] is None else tuple(types.CellType(value) for value in data['CL'])  # type: ignore
    )
    func.__doc__ = data['DO']
    func.__module__ = data['M']
    func.__qualname__ = data['Q']
    func.__annotations__ = data['A']
    return func

