import os
import sys


class CrossInterpreterWriter:
    def __init__(self, fd):
        self._fd = fd

    def write(self, data: bytes):
        import sys
        import os
        full_data = len(data).to_bytes(8, sys.byteorder, signed=False) + data
        os.write(self._fd, full_data)

    def close(self):
        os.close(self._fd)

    @property
    def fileno(self):
        return self._fd


class CrossInterpreterReader:
    def __init__(self, fd):
        self._fd = fd

    def read(self):
        import sys
        size_b = os.read(self._fd, 8)
        if len(size_b) != 8:
            return None
        size = int.from_bytes(size_b, sys.byteorder, signed=False)
        res = os.read(self._fd, size)
        if len(res) != size:
            return None
        return res

    def close(self):
        os.close(self._fd)

    @property
    def fileno(self):
        return self._fd


class Interpreter:
    """
    Represents an interpreter that's part of a given python process.
    """
    def __new__(cls, iid, *args, **kwargs):
        from . import system
        if iid in system.InterpreterStatus.interpreters:
            return system.InterpreterStatus.interpreters[iid]
        self = super().__new__(cls)
        self._status = system.InterpreterStatus(iid)
        system.InterpreterStatus.interpreters[iid] = self
        return self

    def destroy(self):
        if self._status is None:
            return
        if not self._status.validate():
            self._status = None
            return
        import _xxsubinterpreters
        from . import system
        if self._status.id == _xxsubinterpreters.get_current():
            raise RuntimeError("Cannot destroy the current interpreter.")
        if self._status.id == _xxsubinterpreters.get_main():
            raise RuntimeError("Cannot destroy the main interpreter.")
        _xxsubinterpreters.destroy(self._status.id)
        del system.InterpreterStatus.interpreters[self._status.id]
        self._status = None

    def run_string(self, script: str, shared: bool) -> int:
        import _xxsubinterpreters
        return _xxsubinterpreters.run_string(self._status.id, script, shared)

    @classmethod
    def from_id(cls, iid):
        return cls(iid)

    @classmethod
    def create(cls):
        import _xxsubinterpreters
        return cls(_xxsubinterpreters.create())

    @classmethod
    @property
    def current(cls):
        import _xxsubinterpreters
        return cls(_xxsubinterpreters.get_current())

    @property
    def switch_interval(self):
        if self._status is None or not self._status.validate():
            raise RuntimeError("Destroyed interpreter.")
        return self._status.switch_interval.value

    @switch_interval.setter
    def switch_interval(self, value):
        if self._status is None or not self._status.validate():
            raise RuntimeError("Destroyed interpreter.")
        self._status.switch_interval.value = value

    @property
    def recursion_limit(self):
        if self._status is None or not self._status.validate():
            raise RuntimeError("Destroyed interpreter.")
        return self._status.recursion_limit.value

    @recursion_limit.setter
    def recursion_limit(self, value):
        if self._status is None or not self._status.validate():
            raise RuntimeError("Destroyed interpreter.")
        self._status.recursion_limit.value = value

    @property
    def id(self):
        if self._status is None or not self._status.validate():
            raise RuntimeError("Destroyed interpreter.")
        return int(self._status.id)

    @property
    def owner_process(self):
        return None
