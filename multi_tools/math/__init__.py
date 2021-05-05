# from multi_tools.math.numbers import *


class Counter:
    def __init__(self, name: str, value: int):
        self.value = value
        self._name = name

    def incr(self):
        self.value += 1

    def decr(self):
        self.value -= 1

    def __repr__(self):
        return f"<Counter '{self._name}' at {id(self)}, value={self.value}>"
