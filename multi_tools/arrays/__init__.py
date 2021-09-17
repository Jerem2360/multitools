
from multi_tools.arrays import dict as _dct


class _ArrayClass(object):
    __type__ = object

    def __init__(self, list_: __type__):
        if not isinstance(list_, self.__type__):
            raise TypeError(f"Expected type 'list[{self.__type__.__qualname__}]'. ")

        self.values = list_


class _ArrayTypeDef(object):
    def __init__(self):
        raise ValueError("Missing typename parameter 'type' for type 'Array'.")

    def __class_getitem__(cls, item: type):
        class _Array(_ArrayClass):
            __type__ = item

        def init(self, list_: item):
            super().__init__(list_)

        _Array.__init__ = init

        return _Array


class Array(_ArrayTypeDef):
    """
    A typed array.
    If given a typename parameter but not instantiated, works as a generic type.

    This special class should be instantiated like so:

    var = Array[type](arg1)

    e.g.:

    myarray = Array[int]([10, 20, 30])  # new typed array of type 'int'
    print(isinstance(myarray, Array))  # -> True
    """

    pass


