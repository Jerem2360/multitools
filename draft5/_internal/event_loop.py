

class Promise:
    def __init__(self):
        self._val = None
        self._ret = False

    def _satisfy(self, val):
        if self._ret:
            return
        self._val = val
        self._ret = True

    @property
    def value(self):
        if not self._ret:
            raise ValueError("Callable has not returned yet.")
        return self._val

    @property
    def done(self):
        return self._ret


class Event:
    __slots__ = (
        '__weakref__',
    )

    def __init__(self):
        raise TypeError("Abstract class.")

    def run(self):
        raise TypeError("Abstract method.")

    def name(self):
        raise TypeError("Abstract method.")


class InvocationEvent(Event):
    __slots__ = (
        '_func',
        '_args',
        '_kwargs',
        '_result',
    )

    def __init__(self, func, *args, **kwargs):
        self._func = func
        self._args = args
        self._kwargs = kwargs
        self._result = Promise()

    def run(self):
        try:
            res = self._func(*self._args, **self._kwargs)
        except BaseException as e:
            raise ExceptionEvent.InterruptingException(e)

        self._result._satisfy(res)

    def name(self):
        if hasattr(self._func, '__qualname__'):
            return self._func.__qualname__
        if hasattr(self._func, '__name__'):
            return self._func.__name__
        return repr(self._func)


class ExceptionEvent(Event):

    class InterruptingException(Exception):
        def __init__(self, exc):
            self.exc = exc
            super().__init__()


    __slots__ = (
        '_exc',
        '_result',
    )

    def __init__(self, exc: BaseException):
        self._exc = exc
        self._result = None

    def run(self):
        raise type(self).InterruptingException(self._exc)

    def name(self):
        return type(self._exc).__qualname__


class EventLoop:
    def __init__(self):
        self._events = []

    def schedule_invoke(self, func, *args, **kwargs):
        e = InvocationEvent(func, *args, **kwargs)
        self._events.append(e)
        return e._result

    def schedule_exception(self, exc: Exception):
        self._events.append(ExceptionEvent(exc))

    def schedule_exit(self, code: int):
        self._events.append(ExceptionEvent(SystemExit(code)))

    def schedule_keyboard_interrupt(self):
        self._events.append(ExceptionEvent(KeyboardInterrupt()))

    def run_event(self):
        # if there are no events to run, just return False
        if not len(self._events):
            return False
        import sys
        import _thread

        # pop the first event, so events are handled in a FIFO manner
        event = self._events.pop(0)
        exc = None

        # dedicated audit for entering an event
        sys.audit("multitools.enter-event", event)

        # actually running the event
        try:
            event.run()
        except ExceptionEvent.InterruptingException as e:
            # exceptions thrown by events should be encapsulated in an InterruptingException object
            exc = e.exc

        except:
            # if not encapsulated, just raise RuntimeError.
            raise RuntimeError(f"Thread {hex(_thread.get_ident())}: invalid handling of an exception in event '{event.name()}'.")

        # sys.audit can raise, in which case we must take in account the raised exception
        try:
            sys.audit("multitools.leave-event", event, exc)
        except BaseException as e:
            # the context of the raised exception must be whichever exception was raised by the event itself
            # the wanted format is:
            #
            # <event exception traceback>
            # during handling of the above exception, another exception occurred:
            # <sys.audit exception traceback>

            # if the event did not throw an exception, then this just acts as an override.
            context = exc
            exc = e
            exc.__context__ = context

        # SystemExit may be re-raised as-is as it involves no traceback display to stderr.
        # note we don't want to display SystemExit to stderr.
        if isinstance(exc, SystemExit):
            raise exc

        if isinstance(exc, BaseException):
            # we cannot simply raise the exception as the current thread might try to handle it in our place.
            # whether we raise or not, this exception will never be catchable by the thread's code because it is raised in
            # the base system trace function.
            print(f"The following exception was raised during handling of event '{event.name()}' in thread {hex(_thread.get_ident())}:", file=sys.stderr)
            sys.excepthook(type(exc), exc, exc.__traceback__)

            # in case of an exception, terminate the current thread
            raise SystemExit(1)
        return True


