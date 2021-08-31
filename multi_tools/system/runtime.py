from types import FunctionType, MethodType
from typing import Union
from threading import Thread
import sys


class thread_(object):
    def __init_subclass__(cls, **kwargs):
        raise TypeError("'thread' class can't be subclassed.")

    def __init__(self, function: FunctionType):
        """
        Create and return a threaded function.
        """
        self._function = function

    def __call__(self, *args, **kwargs):
        """
        Implement self(*args, **kwargs)
        """
        Thread(target=self._function, args=args, kwargs=kwargs).start()


def thread(f: Union[FunctionType, MethodType]):
    def inner(*args, **kwargs):
        th = thread_(f)
        return th(*args, **kwargs)
    return inner


class ThreadContainer:

    def __init_subclass__(cls, start_immediately=False):
        """
        Implement

        class C(cls, start_immediately=False):
        """
        cls._immediate_start = start_immediately

    def __init__(self, args: tuple = None, kwargs: dict = None):
        """
        Superclass for threaded classes.
        """
        self._locked = False
        self._thread = None

        if self._immediate_start:
            if args is None:
                args = ()
            if kwargs is None:
                kwargs = {}
            self.start(*args, **kwargs)

    def _call(self, *args, **kwargs):
        """
        Method that is called at the start of the thread.
        """
        self.main(*args, **kwargs)
        self._locked = False

    def main(self, *args, **kwargs):
        """
        The thread's lifetime, actions.
        You may override this to customize what the thread does.
        """
        pass

    def start(self, *args, **kwargs):
        """
        Method that starts the thread.
        """
        if not self._locked:
            self._locked = True
            self._thread = Thread(target=self._call, args=args, kwargs=kwargs)
            self._thread.start()

    @property
    def thread(self):
        return self._thread

    def __getitem__(self, item):
        if not item.startswith('_'):
            return self._thread.__getattribute__(item)

    @staticmethod
    def print(*args, sep=' ', end='\n', flush=False, file=sys.stdout):
        """
        A cleaner version of print(), but for threads.
        """
        text = ""
        counter = 0
        for word in args:
            word = str(word)
            text += word
            if counter < (len(args) - 1):
                text += sep
        text += end

        file.write(text)
        if flush:
            file.flush()
