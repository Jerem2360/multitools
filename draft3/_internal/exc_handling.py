

class ExcState:
    def __new__(cls, exception, origin):
        if hasattr(exception, '__state__'):
            return exception.__state__
        self = super().__new__(cls)
        self.tb = []
        self.origin = origin
        exception.__state__ = self

        return self

    def _clear(self):
        from .tstate import TState
        tstate = TState.current()
        for tb in self.tb:
            f = tb.tb_frame
            if f in tstate._masked_frames:
                tstate._masked_frames.pop(tstate._masked_frames.index(f))

    def take_snapshot(self, frame):
        import types
        self.tb.append(types.TracebackType(None, frame, frame.f_lasti, frame.f_lineno))
        # print(self.tb)

    def build_traceback(self):
        import types
        tb = None
        for _tb in self.tb:
            tb = types.TracebackType(tb, _tb.tb_frame, _tb.tb_lasti, _tb.tb_lineno)
        return tb

    def __del__(self):
        self._clear()


def excepthook(exc_type, exc_value, tb):
    import sys
    from .interp import Interpreter

    if hasattr(exc_value, '__state__'):
        estate = exc_value.__state__
        tb = estate.build_traceback()
        exc_value.__traceback__ = tb

    return Interpreter.excepthook(exc_type, exc_value, tb)


def trace_exceptions(tstate, frame, arg):
    exc_type, exc_val, tb = arg

    estate = ExcState(exc_val, frame)
    if not (tstate._mask_frame or (frame in tstate._masked_frames)):
        estate.take_snapshot(frame)


class FrameMask:
    def __init__(self, depth=0):
        from .tstate import TState
        tstate = TState.current()
        self._frame = tstate.call_stack[depth+1]

    def __enter__(self):
        from .tstate import TState
        tstate = TState.current()
        tstate._masked_frames.append(self._frame)
        # print("enter", tstate._masked_frames)

    def __exit__(self, exc_type, exc_val, exc_tb):
        if None in (exc_type, exc_val):
            from .tstate import TState
            tstate = TState.current()
            tstate._masked_frames.pop(tstate._masked_frames.index(self._frame))
            # print("exit", tstate._masked_frames)

