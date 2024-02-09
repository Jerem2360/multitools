from ._internal.thread import *
from ._internal.runtime import *


class Thread:
    def __init__(self, func):
        self._func = func
        self._id = 0

    def __call__(self, *args, **kwargs):
        import _thread
        self._id = _thread.start_new_thread(self._func, args, kwargs)

    def exit(self):
        state = TState._objects[self._id]
        state.exit()

    @classmethod
    def sleep(cls, ms):
        import time
        timer = time.time()
        tstate = TState.current()
        while not tstate.exiting:
            if time.time() >= timer + ms:
                break

