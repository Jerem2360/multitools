import sys
import types
from . import protocols


class CurdirOverride:
    def __init__(self, path):
        import os
        self.path = path
        self.cache = None

    def __enter__(self):
        import os
        self.cache = os.getcwd()
        os.chdir(self.path)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        import os
        os.chdir(self.cache)


def get_frame(proxy, tid, depth=0):
    import _thread
    if tid == _thread.get_ident():
        depth += 2

    # noinspection PyUnresolvedReferences
    res = sys._current_frames().get(tid, None)

    for i in range(depth):
        if res.f_back is None:
            break
        res = res.f_back

    proxy._cache = res
    return res


def curdir_at_module_location(depth=0):
    import os
    from .interp import Interpreter
    tstate = Interpreter.TState.current()
    frame = tstate.call_stack[depth + 1]
    file = frame.f_code.co_filename
    if not os.path.exists(file):
        raise TypeError("Could not find the module's file.")
    directory = file.rsplit(os.path.sep, 1)[0]
    if not os.path.isdir(directory):
        raise TypeError("Module is not located inside a valid directory.")
    return CurdirOverride(directory)


class CallStackIterator:
    def __init__(self, f):
        self._f = f

    def __next__(self) -> types.FrameType:
        if self._f is None:
            raise StopIteration
        res = self._f
        self._f = self._f.f_back
        return res


class CallStackProxy:
    __slots__ = (
        '_tid',
        '_cache',
    )

    def __init__(self, tid):
        self._tid = tid
        get_frame(self, self._tid)

    def __getitem__(self, item: int) -> types.FrameType | None:
        current = get_frame(self, self._tid)

        for i in range(item):
            if current.f_back is None:
                return current
            current = current.f_back
        return current

    def __len__(self) -> int:
        i = 0
        current = get_frame(self, self._tid)

        while True:
            if current is None:
                return i
            current = current.f_back
            i += 1

    def __iter__(self) -> protocols.IteratesOverCallStack:
        return CallStackIterator(self[0])


class ExcInfoProxy(tuple):
    def __new__(cls, tid, *args, **kwargs):
        return super().__new__(cls, (None, None, None))

    def __init__(self, tid):
        super().__init__()
        self._tid = tid

    # noinspection PyUnresolvedReferences
    def __getitem__(self, item: int):
        if self._tid not in sys._current_exceptions():
            return None
        return sys._current_exceptions()[self._tid][item]

    # noinspection PyUnresolvedReferences
    def __len__(self):
        return 3 if self._tid in sys._current_exceptions() else 0

    # noinspection PyUnresolvedReferences
    def __contains__(self, item):
        if self._tid not in sys._current_exceptions():
            return False
        return item in sys._current_exceptions()[self._tid]

    # noinspection PyUnresolvedReferences
    def __eq__(self, other):
        if self._tid not in sys._current_exceptions():
            return False
        return sys._current_exceptions()[self._tid] == other

    def __ge__(self, other):
        return NotImplemented

    def __gt__(self, other):
        return NotImplemented

    def __le__(self, other):
        return NotImplemented

    def __lt__(self, other):
        return NotImplemented

    # noinspection PyUnresolvedReferences
    def __hash__(self):
        if self._tid not in sys._current_exceptions():
            return hash(())
        return hash(sys._current_exceptions()[self._tid])

    def __mul__(self, other):
        return NotImplemented

    # noinspection PyUnresolvedReferences
    def __iter__(self):
        return iter(sys._current_exceptions().get(self._tid, ()))

    # noinspection PyUnresolvedReferences
    def __repr__(self):
        if self._tid not in sys._current_exceptions():
            return repr(())
        return repr(sys._current_exceptions()[self._tid])

    @property
    def type(self) -> type[BaseException] | None:
        return self[0]

    @property
    def value(self) -> BaseException | None:
        return self[1]

    @property
    def traceback(self) -> types.TracebackType | None:
        return self[2]


class ThreadEvent:
    __slots__ = (
        '_type',
        '_arg',
        '_result',
    )

    def __init__(self):
        self._type = 0
        self._arg = None
        self._result = ScheduledResult()

    @classmethod
    def new_throw(cls, exc):
        """
        Create and return a new "throw" thread event object.
        """
        res = cls()
        res._type = 1
        res._arg = exc
        return res

    @classmethod
    def new_invoke(cls, target, args, kwargs):
        """
        Create and return a new "invoke" thread event object.
        """
        res = cls()
        res._type = 2
        res._arg = (target, args, kwargs)
        return res

    def run(self):
        """
        Run the event in the current thread.
        The event's return value is stored in the 'result' attribute.
        """
        match self._type:
            case 0:  # nothing
                self._result.set(None)
                return 0
            case 1:  # exception
                self._result.set(None)
                raise self._arg
            case 2:  # invoke
                try:
                    res = self._arg[0](*self._arg[1], **self._arg[2])
                except SystemExit:
                    raise
                except:
                    import _thread
                    print(f"Exception caught in invoke call in thread {_thread.get_ident()}:", file=sys.stderr)
                    sys.excepthook(*sys.exc_info())
                    return 1
                self._result.set(res)
                return 0

    @property
    def result(self):
        return self._result

    def __repr__(self):
        name = "ThreadEvent"
        match self._type:
            case 0:
                name = "ThreadEvent '<NOOP>'"
            case 1:
                name = f"ThreadEvent '{repr(self._arg)}'"
            case 2:
                name = f"ThreadEvent '{self._arg[0].__name__}(...)'"

        return f"<{name} at {hex(id(self))}>"


class ScheduledResult:
    """
    The future result of a call.
    This has no value until the callee returns.
    """

    def __init__(self):
        self._valid = False
        self._contents = None

    def set(self, value):
        self._valid = True
        self._contents = value
        return self

    def wait(self):
        """
        Wait until the callee returns and return its result.
        The callee itself must never, even indirectly, call this itself,
        or a deadlock will ensue.
        Waiting for functions that never return will cause a deadlock.
        """
        while not self._valid:
            pass
        return self._contents

    @property
    def returned(self):
        """
        Whether the callee has already returned.
        """
        return self._valid

    @property
    def value(self):
        """
        The value returned by the callee.
        Raises RuntimeError if callee has not already returned.
        """
        if not self._valid:
            raise RuntimeError("Callee hasn't returned yet.")
        return self._contents

    def __repr__(self):
        if self._valid:
            return f"<Scheduled result '{self._contents}'>"
        return f"<Scheduled result: waiting for callee to return>"

