from multi_tools import env
from typing import overload, Union, Literal, Any
from multi_tools.math.errors import InfiniteDivisionError


if env.module_installed("_c_maths"):
    # to avoid errors, define further objects only if _c_maths is installed
    import _c_maths

    """
    Constants:
    """
    # here are values coming from _c_maths:
    e = _c_maths.e  # E(1)
    i = _c_maths.i  # i, or sqrt(-1)

    PLUS = "+"
    MINUS = "-"

    """
    Functions:
    """

    exp = _c_maths.exp  # exp(x: float) -> float

    # here will go classes that use _c_maths

    """
    Classes:
    """

    class complex_(_c_maths.ComplexType):
        def __init__(self, real, imag):
            """
            Similar to the builtin 'complex', but more efficient and quick.
            """
            _c_maths.ComplexType.__init__(real, imag)

        def __repr__(self):
            """
            Implement repr(self).
            """
            return f"{self.real}+{self.imag}i"


    class infinite(_c_maths.InfiniteType):
        _checker = False
        @overload
        def __init__(self, sign: Union[Literal["+"], Literal["-"]]): ...

        @overload
        def __init__(self, x: Any): ...

        def __init__(self, __v=None):
            """
            A class that represents both positive an negative infinity.
            Very simple to understand, but not very advanced.

            Signatures:

            - infinite(sign: PLUS or MINUS) -> infinite

              Create and return an infinite number.

            - infinite(x: Any) -> bool

              return whether x is an infinite.
            """
            self._x = None
            if __v == PLUS:
                _c_maths.InfiniteType.__init__(self, True)
            elif __v == MINUS:
                _c_maths.InfiniteType.__init__(self, False)
            else:
                self._checker = True
                self._x = __v

        def __bool__(self):
            """
            Implement bool(self)
            """
            if self._checker:
                return isinstance(self._x, (infinite, _c_maths.InfiniteType))
            return True

        def __repr__(self):
            """
            Implement repr(self)
            """
            if self._checker:
                return repr(self.__bool__())
            if self.pos:
                return "+\u221E"
            return "-\u221E"

        # math operations, useful only if __init__ returned an infinite:
        if not _checker:
            def __add__(self, other):
                return self

            def __radd__(self, other): return self.__add__(other)

            def __iadd__(self, other): return self

            def __neg__(self):
                x = self
                x.invert()
                return x

            def __sub__(self, other):
                return self.__add__(-other)

            def __rsub__(self, other):
                return self.__radd__(-other)

            def __isub__(self, other): return self

            def __invert__(self): return 0

            def __ge__(self, other):
                return self.pos

            def __gt__(self, other):
                return self.pos

            def __le__(self, other):
                return not self.pos

            def __lt__(self, other):
                return not self.pos

            def __mul__(self, other):
                if other > 0:
                    return self
                elif other < 0:
                    x = self
                    x.invert()
                    return x
                elif other == 0:
                    return 0

            def __rmul__(self, other):
                return self.__mul__(other)

            def __imul__(self, other):
                return self.__mul__(other)

            def __truediv__(self, other):
                if other == 0:
                    raise ZeroDivisionError("Division by zero.")
                elif infinite(other):
                    raise InfiniteDivisionError()
                elif other < 0:
                    x = self
                    x.invert()
                    return x
                elif other > 0:
                    return self

            def __rtruediv__(self, other):
                if not (other == 1):
                    raise InfiniteDivisionError()
                return 0

            def __itruediv__(self, other):
                return self.__truediv__(other)


else:  # warn the user that _c_maths isn't installed:
    import warnings
    warnings.warn("The extension \"_c_maths\" isn't installed, all functions related to it will be unusable.")
