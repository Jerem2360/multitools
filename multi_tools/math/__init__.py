from multi_tools.math.numbers import *

"""
Module that contains useful maths functions and classes.
"""

class Counter:
    def __init__(self, name: str, value: int):
        """
        Create a counter called name, initialized with value value.
        """
        self.value = value
        self._name = name

    def incr(self):
        """
        Increase the counter's value by 1.
        """
        self.value += 1

    def decr(self):
        """
        Decrease the counter's value by 1.
        """
        self.value -= 1

    def __repr__(self):
        """
        Implement repr(self)
        """
        return f"<Counter '{self._name}' at {id(self)}, value={self.value}>"
