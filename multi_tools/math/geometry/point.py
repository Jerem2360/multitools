from multi_tools.math.geometry import bases


class Point2D(bases.GeometryObject):
    def __init__(self, x, y):
        """
        Represents a point on a 2D surface.
        -> x: Union[int, float]
        -> y: Union[int, float]
        """
        super().__init__()

        self._coordinates = [x, y]

    x = property(lambda self: self._coordinates[0])
    y = property(lambda self: self._coordinates[1])


class Point3D(bases.GeometryObject):
    def __init__(self, x, y, z):
        """
        Represents a point in 3D space.
        -> x: Union[int, float]
        -> y: Union[int, float]
        -> z: Union[int, float]
        """
        super().__init__()

        self._coordinates = [x, y, z]

    x = property(lambda self: self._coordinates[0])
    y = property(lambda self: self._coordinates[1])
    z = property(lambda self: self._coordinates[2])

