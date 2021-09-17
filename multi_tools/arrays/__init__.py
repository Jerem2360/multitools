from multi_tools import typing
from multi_tools.arrays import dict as _dct

class TypedArray(typing.Generic):
    __type__ = typing.Any

    @classmethod
    def __check__(cls, args: list[type]):
        cls.__type__ = args[0]

    @classmethod
    def __edit_type__(cls, args: list[type], tp: type[typing.GenericInstance]) -> type[typing.GenericInstance]:

        class _Arr(tp):

            def __init__(self, v: list[cls.__type__]):
                super().__init__()
                self._type_check(v)
                self._value = {}

                for i in v:
                    self._value[i] = None

            def __getitem__(self, item: int):
                lt = self.to_list()
                return lt[item]

            def __setitem__(self, key: int, value: cls.__type__):
                lt = self.to_list()
                if not isinstance(value, cls.__type__):
                    raise TypeError(
                        f"Expected type '{cls.__type__.__name__}', got '{type(value).__name__}' instead."
                    )
                lt[key] = value

                self._value = {}

                for i in lt:
                    self._value[i] = None

            def __delitem__(self, key: int):
                lt = self.to_list()
                lt.pop(key)

                self._value = {}
                for i in lt:
                    self._value[i] = None

            def __iter__(self):
                self._counter = 0
                return self

            def __next__(self):
                try:
                    r = self.to_list()[self._counter]
                except KeyError or IndexError:
                    raise StopIteration

                self._counter += 1
                return r

            def __len__(self):
                return len(self.to_list())

            def __add__(self, other: list[cls.__type__] or TypedArray[cls.__type__]):

                r = []

                if isinstance(other, list):
                    self._type_check(other)
                    o = cls[cls.__type__](other)

            @staticmethod
            def _type_check(v: list):
                for i in v:
                    if not isinstance(i, cls.__type__):
                        raise TypeError(
                            f"Expected type 'list[{cls.__type__.__name__}]', got 'list[{type(i).__name__}, ...]' instead."
                        )

            def to_list(self):
                result = []
                for i in self._value:
                    result.append(i)
                return result

        return _Arr

