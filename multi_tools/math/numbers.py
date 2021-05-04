from multi_tools import env
from typing import overload, Union, Literal, Any
from multi_tools.math.errors import InfiniteDivisionError


if env.module_installed("_c_maths"):
    import _c_maths

    # here are values coming from _c_maths:
    e = _c_maths.e
    i = _c_maths.i

    exp = _c_maths.exp

    # here will go classes that use _c_maths

    class complex_(_c_maths.ComplexType):
        def __init__(self, real, imag):
            _c_maths.ComplexType.__init__(real, imag)


    PLUS = "+"
    MINUS = "-"

    """
    Classes
    """
    class infinite(_c_maths.InfiniteType):
        _checker = False
        @overload
        def __init__(self, sign: Union[Literal["+"], Literal["-"]]): ...

        @overload
        def __init__(self, x: Any): ...

        def __init__(self, __v=None):
            self._x = None
            if __v == PLUS:
                _c_maths.InfiniteType.__init__(self, True)
            elif __v == MINUS:
                _c_maths.InfiniteType.__init__(self, False)
            else:
                self._checker = True
                self._x = __v

        def __bool__(self):
            if self._checker:
                return isinstance(self._x, (infinite, _c_maths.InfiniteType))
            return True

        def __repr__(self):
            if self._checker:
                return repr(self.__bool__())
            if self.pos:
                return "+\u221E"
            return "-\u221E"

        # math operations:
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



else:
    import warnings
    warnings.warn("The extension \"_c_maths\" isn't installed, all functions related to it will be unusable.")
