
class ThreadExceptionProxy:
    def __init__(self, status):
        self._status = status

    @property
    def exception(self):
        import sys
        return sys._current_exceptions().get(self._status.id, None)

    @property
    def traceback(self):
        import sys
        exc = sys._current_exceptions().get(self._status.id, None)
        if exc is not None:
            return exc.__traceback__
        return None


class CallStackProxy:
    class _Iterator:
        def __init__(self, status):
            self.frame = status.current_frame

        def __next__(self):
            if self.frame is None:
                raise StopIteration
            res = self.frame
            self.frame = self.frame.f_back
            return res

    def __init__(self, status):
        from . import system
        self._status: system.ThreadStatus = status

    def __len__(self):
        frame = self._status.current_frame

        i = 0
        while frame.f_back is not None:
            i += 1
            frame = frame.f_back
        return i + 1

    def __getitem__(self, item):
        frame = self._status.current_frame
        for i in range(item):
            if frame is None:
                raise IndexError(item)
            frame = frame.f_back
        return frame

    def __iter__(self):
        return self._Iterator(self._status)


class TState:

    def __new__(cls, tid, *args, **kwargs):
        from . import system
        if tid in system.ThreadStatus.threads:
            return system.ThreadStatus.threads[tid]
        self = super().__new__(cls)
        self._status = system.ThreadStatus(tid)
        system.ThreadStatus.threads[tid] = self
        return self

    def queue_interrupt(self, event):
        self._status.event_queue.append(event)

    def settrace(self, cb, event):
        if event not in self._status.trace_functions:
            return False
        self._status.trace_functions[event].append(cb)
        return True

    @classmethod
    def from_id(cls, tid):
        return cls(tid)

    @classmethod
    @property
    def current(cls):
        import _thread
        return cls(_thread.get_ident())

    @property
    def id(self):
        return self._status.id

    @property
    def call_stack(self):
        return CallStackProxy(self._status)

    @property
    def exception_status(self):
        return ThreadExceptionProxy(self._status)

