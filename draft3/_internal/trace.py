import sys


class UnregisterTrace(BaseException):
    pass


def call_trace(func, _tstate, *args, **kwargs):
    from . import tstate
    try:
        func(_tstate, *args, **kwargs)
    except SystemExit:
        raise
    except tstate.StopTracing:
        return False
    except BaseException:
        print(f"Exception caught in tracing function '{func.__qualname__}':", file=sys.stderr)
        sys.excepthook(*sys.exc_info())
        raise UnregisterTrace from None
    return True


def unregister_trace(tstate, func, event):
    traces = tstate._traces.get(event, [])
    if func not in traces:
        return
    traces.pop(traces.index(func))


def __trace__(frame, event, arg):
    import _thread
    if not frame.f_trace_opcodes:
        frame.f_trace_opcodes = True
    if frame.f_code.co_filename.startswith("<frozen "):
        return
    if sys.meta_path is None:
        return

    from .interp import Interpreter
    if Interpreter is Ellipsis:  # interpreter proxy not initialized
        return
    tstate = Interpreter.TState.current()
    
    if len(tstate._event_queue) and tstate._do_events:
        event = tstate._event_queue[-1]
        if event.run():
            raise SystemExit(1)  # invoke has failed with an exception
        tstate._event_queue.pop(-1)

    if not tstate._do_trace:
        return
    tstate._tracing = True

    for tracefunc in tstate._traces.get(event, []):
        try:
            if not call_trace(tracefunc, tstate, frame, arg):
                break
        except UnregisterTrace:
            unregister_trace(tstate, tracefunc, event)

    for tracefunc in tstate._traces['*']:
        try:
            if not call_trace(tracefunc, tstate, event, arg):
                break
        except UnregisterTrace:
            unregister_trace(tstate, tracefunc, event)
    tstate._tracing = False
    return __trace__

