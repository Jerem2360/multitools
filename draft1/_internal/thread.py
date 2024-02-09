from . import errors, runtime


_old_shutdown = lambda: None


def __begin__():
    """
    Initialize the state for the current thread.
    Runs at the beginning of each new thread,
    including the main thread.
    """
    global _old_shutdown
    import threading as _th
    from . import runtime
    if _th._shutdown != terminate:
        _old_shutdown = _th._shutdown
        _th._shutdown = terminate
    runtime.__thread_begin__()
    errors.__thread_begin__()


def __terminate__():
    """
    cleanup a terminating thread's runtime.
    """
    runtime.__thread_terminate__()
    _old_shutdown()


begin = __begin__
"""
Called each time a new python thread begins.
Can be changed, but MUST call the original __begin__ once and only once.
"""
terminate = __terminate__
"""
Can be changed, but MUST call the original __terminate__ once and only once.
"""

