"""
Error customization interface.
This is a private api. It will be exposed later through
a more intuitive interface.
"""


import sys

from . import runtime


def __thread_begin__():
    """
    Runs at the start of each new thread.
    """
    tstate = runtime.TState.current()

    # install our tracing function that triggers whenever an exception is raised,
    # even if it is caught later on. It is always triggered before sys.excepthook.
    @tstate.trace('exception')
    def trace_exc(frame, args):
        # print(args)
        etype, evalue, etb = args
        cnf = evalue.__cause__  # we rely on the user-defined attribute __cause__ to relay the exception config
        if not hasattr(evalue, '__info__'):
            evalue.__info__ = TracebackDetails()
            # print("scope", evalue.__info__.raised_frame, frame)
            evalue.__info__.raised_frame = frame

            if isinstance(cnf, ExceptionConfiguration):
                if cnf.cause is NotImplemented:
                    evalue.__cause__ = None
                    evalue.__suppress_context__ = False
                else:
                    evalue.__cause__ = cnf.cause if isinstance(cnf.cause, BaseException) else cnf.cause() if isinstance(cnf.cause, type) and issubclass(cnf.cause, BaseException) else None
                    evalue.__suppress_context__ = True
                if cnf.context is not NotImplemented:
                    evalue.__context__ = cnf.context
                evalue.__info__.depth = cnf.depth
                evalue.__info__.fignore = cnf.fignore


def except_hook(etype, evalue, etb):
    # print("caught!")
    import types
    import sys
    frame = evalue.__info__.calculate_top_frame()

    tb = None
    while True:
        if frame is None:
            break
        if frame not in evalue.__info__.fignore:
            tb = types.TracebackType(tb, frame, frame.f_lasti, frame.f_lineno)
        frame = frame.f_back

    evalue.__traceback__ = tb
    sys.__excepthook__(type(evalue), evalue, tb)


sys.excepthook = except_hook


class ExceptionConfiguration(BaseException):
    def __init__(self):
        self.cause = NotImplemented  # NotImplemented doesn't set __suppress_context__ to True
        self.context = NotImplemented  # NotImplemented means keep existing context
        self.depth = 0
        self.fignore = []


class TracebackDetails:
    def __init__(self):
        self.depth = 0
        self.raised_frame = None
        self.fignore = []

    def calculate_top_frame(self):
        frame = self.raised_frame

        for i in range(self.depth):
            temp = frame.f_back
            if temp is None:
                return frame
            frame = temp
        return frame


class _FrameMask:
    __slots__ = (
        "_frame",
    )

    def __init__(self):
        self._frame = None

    def __enter__(self):
        tstate = runtime.TState.current()
        self._frame = tstate.call_stack[1]  # the frame to ignore is our caller's frame
        return self._frame

    def __exit__(self, exc_type, exc_val, exc_tb):
        if None in (exc_type, exc_val):
            return
        if not hasattr(exc_val, '__info__'):  # in case our trace function is not installed
            import warnings
            warnings.warn("An attempt to hide a frame from a stack trace was made, but multitools tracing function is not installed.", RuntimeWarning)
            return
        # print(f"context manager exit, info is {getattr(exc_val, '__info__', None)}")
        exc_val.__info__.fignore.append(self._frame)


def frame_mask():
    """
    If an exception is raised within this context manager, the current
    frame will not appear in the stack trace printed to sys.stderr
    Yields the frame to be hidden if 'as' is used.

    Note: multitools must have been imported at least once in the program
    to enable this behaviour.
    """
    return _FrameMask()


def custom(**kwargs):
    """
    custom(depth: int = 0, cause: BaseException = ..., context: BaseException = ...)

    Customize the display of an exception.
    'depth' controls the frame which should end the stack trace. The chosen frame is
    the one 'depth' deep in the call stack, starting from the current frame.

    'cause' allows to specify an exception marked as the 'direct cause' of the raised exception.
    Normally, this stands in the from clause of the raise statement. Setting this to None
    suppresses the cause and context of the exception.

    'context' allows to override the exception being handled while the exception is raised.

    Usage:
    raise ... from custom(...)
    """
    res = ExceptionConfiguration()
    res.depth = kwargs.get('depth', 0)
    if 'cause' in kwargs:
        res.cause = kwargs.get('cause')
    if 'context' in kwargs:
        res.context = kwargs.get('context')
    return res


