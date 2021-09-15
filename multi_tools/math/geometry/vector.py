from multi_tools.math.geometry import bases, point
from multi_tools.math.geometry.bases import format_id, typename
from typing import overload, Union


class Vector2D(bases.GeometryObject):
    @overload
    def __init__(self, p1: point.Point2D, p2: point.Point2D):
        ...

    @overload
    def __init__(self, x: Union[int, float], y: Union[int, float]):
        ...

    def __init__(self, *args):
        """
        Create a vector object in a virtual 2D surface.
        Two signatures are possible:


        Vector2D(number, number) and
        Vector2D(Point, Point)

        For each of them, the vector's coordinates are deduced and assigned to self._coordinates.


        self.x is the x coordinate of the vector,
        and self.y is the y coordinate of the vector.

        To get the length of the vector, use len(vector).
        """
        if len(args) == 2:
            if isinstance(args[0], (int, float)) and isinstance(args[0], (int, float)):

                self._coordinates = [float(args[0]), float(args[1])]

            elif isinstance(args[0], point.Point2D) and isinstance(args[1], point.Point2D):
                x = args[1].x - args[0].x
                y = args[1].y - args[0].y
                self._coordinates = [float(x), float(y)]
            else:
                raise TypeError(f"Expected argument types ('Point', 'Point') or ('Union[int, float]', 'Union[int, float]'), got {tuple(typename(i) for i in args)} instead.")
        else:
            raise TypeError(f"Expected argument types ('Point', 'Point') or ('Union[int, float]', 'Union[int, float]'), got {tuple(typename(i) for i in args)} instead.")

    def __len__(self):
        """
        Implement len(self)
        """
        return ((self._coordinates[0] ** 2) + (self._coordinates[1] ** 2)) ** (1 / 2)

    def __repr__(self):
        """
        Implement repr(self)
        """
        return f"<'Vector2D' object at {format_id(self)}, x={self._coordinates[0]}, y={self._coordinates[1]}>"

    def _dot_product(self, other) -> Union[int, float]:
        """
        The dot product between two vectors, here it's self and other.
        """
        return (self._coordinates[0] * other.x) + (self._coordinates[1] * other.y)  # dot product yields a number.

    def _product(self, item) -> __class__:
        """
        The product between a vector and a real number, here it's self and item
        """
        x = item * self._coordinates[0]
        y = item * self._coordinates[1]
        return Vector2D(x, y)  # product between vector and number yields a vector.

    def __mul__(self, other) -> Union[int, float, __class__]:
        """
        Implement self * other

        Choose between dot product and product depending
        on other's type.
        """
        if isinstance(other, (int, float)):
            return self._product(other)
        elif isinstance(other, Vector2D):
            return self._dot_product(other)
        else:
            raise TypeError(f"'{typename(self)}' object cannot be multiplied by '{typename(other)}' object.")

    def __imul__(self, other): return self.__mul__(other)

    def __rmul__(self, other): return self.__mul__(other)

    def _sum(self, other) -> __class__:
        """
        The sum of two vectors, a.k.a. self + other
        """
        x = self._coordinates[0] + other.x
        y = self._coordinates[1] + other.y
        return Vector2D(x, y)

    def __add__(self, other) -> __class__:
        """
        Implement self + other
        """
        if not isinstance(other, Vector2D):
            raise TypeError(f"'{typename(other)}' object cannot be added to '{typename(self)}' object.")

    def __iadd__(self, other) -> __class__: return self.__add__(other)

    def __radd__(self, other) -> __class__:
        """
        Implement other + self
        """
        if not isinstance(other, Vector2D):
            raise TypeError(f"'{typename(self)}' object cannot be added to '{typename(other)}' object.")
        return self._sum(other)

    def _sub(self, other) -> __class__:
        """
        Subtract two vectors, a.k.a self - other
        """
        return self._sum(-other)

    def __neg__(self):
        self._coordinates[0] = -self._coordinates[0]
        self._coordinates[1] = -self._coordinates[1]

    def __sub__(self, other) -> __class__:
        """
        Implement self - other
        """
        if not isinstance(other, Vector2D):
            raise TypeError(f"'{typename(other)}' object cannot be subtracted to '{typename(self)}' object.")
        return self._sub(other)

    def __isub__(self, other) -> __class__: return self.__sub__(other)

    def __rsub__(self, other) -> __class__:
        """
        Implement other - self
        """
        if not isinstance(other, Vector2D):
            raise TypeError(f"'{typename(self)}' object cannot be subtracted to '{typename(other)}' object.")
        return self._sub(other)

    def __pow__(self, power, modulo=None):
        """
        Implement self ** power
        """
        if not isinstance(power, (int, float)):
            raise TypeError(f"Cannot put '{typename(self)}' object to the power of '{typename(power)}' object.")

        result = self
        for i in range(power):
            result *= result

        return result

    def __ipow__(self, other): return self.__pow__(other)

    x = property(lambda self: self._coordinates[0])
    y = property(lambda self: self._coordinates[1])


class Vector3D(bases.GeometryObject):

    @overload
    def __init__(self, x: Union[int, float], y: Union[int, float], z: Union[int, float]): ...

    @overload
    def __init__(self, p1: point.Point3D, p2: point.Point3D): ...

    def __init__(self, *args):
        """
        Create a vector object in a virtual 3D space.
        Two signatures are possible:


        Vector2D(number, number, number) and
        Vector2D(Point, Point)

        For each of them, the vector's coordinates are deduced and assigned to self._coordinates.


        self.x is the x coordinate of the vector,
        self.y is the y coordinate of the vector,
        and self.z is the z coordinate of the vector.

        To get the length of the vector, use len(vector).
        """
        super().__init__()

        if len(args) == 2:
            param1, param2 = args[0], args[1]
            if isinstance(param1, point.Point3D) and isinstance(param2, point.Point3D):
                x = param2.x - param1.x
                y = param2.y - param1.y
                z = param2.z - param1.z

                self._coordinates = [x, y, z]

            else:
                raise TypeError(f"Expected argument types ('Point', 'Point') or ('Union[int, float]', 'Union[int, float]', 'Union[int, float]'), got {tuple(typename(i) for i in args)} instead.")

        elif len(args) == 3:
            param1 = args[0]
            param2 = args[1]
            param3 = args[2]

            if isinstance(param1, (int, float)) and isinstance(param2, (int, float)) and isinstance(param3, (int, float)):
                self._coordinates = [param1, param2, param3]

            else:
                raise TypeError(f"Expected argument types ('Point', 'Point') or ('Union[int, float]', 'Union[int, float]', 'Union[int, float]'), got {tuple(typename(i) for i in args)} instead.")

        else:
            raise TypeError(f"Expected argument types ('Point', 'Point') or ('Union[int, float]', 'Union[int, float]', 'Union[int, float]'), got {tuple(typename(i) for i in args)} instead.")

    def __len__(self):
        len2d = ((self._coordinates[0] ** 2) + (self._coordinates[1] ** 2)) ** (1 / 2)
        return ((len2d ** 2) + (self._coordinates[2] ** 2)) ** (1 / 2)

    x = property(lambda self: self._coordinates[0])
    y = property(lambda self: self._coordinates[1])
    z = property(lambda self: self._coordinates[2])

