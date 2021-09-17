import os
import ctypes
from multi_tools.system import path


class _List:
    def __init__(self, value: list):
        self._value = value
        self._step = lambda _self, appends: None

    def append(self, item, *items):
        items = (item, *items)
        self._step(self, items)
        for i in items:
            self._value.append(i)

    def __iter__(self):
        self.iter = 0
        return self

    def __next__(self):
        try:
            result = self._value[self.iter]
        except IndexError:
            raise StopIteration
        self.iter += 1
        return result

    def pop(self, index):
        return self._value.pop(index)

    def insert(self, index, value):
        return self._value.insert(index, value)

    def step(self, function):
        self._step = function
        return function


class Cpp:
    SYS32 = "C:/Windows/System32/"
    APPDATA = os.getenv('AppData') + '\\.pyCpp\\'  # "C:/Users/jlefo/AppData/Roaming/.pyCpp/"
    search_paths = _List(["", SYS32, APPDATA])
    CDLL = ctypes.CDLL
    WinDLL = ctypes.WinDLL

    dll_type = CDLL

    @search_paths.step
    def check(self, appends):
        for i in appends:
            if not (os.path.exists(i) or (i == "")):
                raise NotADirectoryError(f"Search path '{i}' is not a directory.")


class Path:
    slash_convention = '/'
    win_convention = '\\'

