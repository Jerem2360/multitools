from typing import overload, Union


def format_id(obj):
    hex_ = hex(id(obj))
    inter = str(hex_).split('0x')[-1].upper()
    return '0x' + inter


def typename(obj):
    return eval("type(obj).__name__", {'obj': obj, **globals()}, locals())


class geometry_object(object):

    __slots__ = []

    __type__ = 'default'
    __axes__ = '[]'

    def __init_subclass__(cls, **kwargs):
        if 'axes' in kwargs:
            if not isinstance(kwargs.get('axes'), (list, tuple)):
                raise TypeError(f"'axes' parameter must be a list[str] or tuple[str], not '{type(kwargs.get('axes'))}'.")

            result = '['
            last = len(kwargs.get('axes')) - 1
            count = 0
            generics_types = []
            for axis in kwargs.get('axes'):
                paramtype = eval(f"list[{typename(axis)}]", {'axis': axis, **globals()}, locals())
                if not paramtype in generics_types:
                    generics_types.append(paramtype)
                if not isinstance(axis, str):
                    raise TypeError(f"'axes' parameter must be a list[str] or tuple[str], not '{paramtype}'.")
                result += axis
                if count < last:
                    result += ', '
                else:
                    result += ']'

                count += 1

            cls.__axes__ = result

    def __repr__(self):
        return "<Geometrical object at {0}, axes={1}".format(format_id(self), self.__axes__)


class _2DGeometricalObject(geometry_object, axes=('x', 'y')):
    __type__ = 'default'

    def __init_subclass__(cls, **kwargs):
        if 'type' in kwargs:
            cls.__type__ = kwargs.get('type')

    def __repr__(self):
        return f"<Geometry object at {format_id(self)}, type={self.__type__}, axes={self.__axes__}>"


class Point(_2DGeometricalObject, type='point'):
    def __init__(self, x: Union[int or float], y: Union[int or float]):
        self._coordinates = [float(x), float(y)]

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]


class Vector2D(_2DGeometricalObject, type='vector'):
    __slots__ = ['_coordinates']

    @overload
    def __init__(self, p1: Point, p2: Point): ...

    @overload
    def __init__(self, x: Union[int or float], y: Union[int or float]): ...

    def __init__(self, *args):
        """
        Create a vector object in a virtual 2D space.
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

            elif isinstance(args[0], Point) and isinstance(args[1], Point):
                x = args[1].x - args[0].x
                y = args[1].y - args[0].y
                self._coordinates = [float(x), float(y)]
            else:
                raise TypeError(f"Expected argument types ('Point', 'Point') or ('int', 'int'), got {tuple(typename(i) for i in args)} instead.")
        else:
            raise TypeError(f"Expected argument types ('Point', 'Point') or ('int', 'int'), got {tuple(typename(i) for i in args)} instead.")

    def __len__(self):
        """
        Implement len(self)
        """
        return (self._coordinates[0] ** 2) + (self._coordinates[1] ** 2)

    def __repr__(self):
        """
        Implement repr(self)
        """
        return f"<'Vector2D' object at {format_id(self)}, x={self._coordinates[0]}, y={self._coordinates[1]}>"

    def _dot_product(self, other):
        """
        The dot product between two vectors, here it's self and other.
        """
        return (self._coordinates[0] * other.x) + (self._coordinates[1] * other.y)

    def _product(self, item):
        """
        The product between a vector and a real number, here it's self and item
        """
        x = item * self._coordinates[0]
        y = item * self._coordinates[1]
        return Vector2D(x, y)

    def __mul__(self, other):
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
            raise TypeError(f"'Vector2D' object cannot be multiplied by '{typename(other)}' object.")

    @property
    def x(self):
        return self._coordinates[0]

    @property
    def y(self):
        return self._coordinates[1]

