from types import FunctionType


class Registry:
    """
    A type representing a registry.
    """
    def __init__(self, accepted_types: type or tuple[type] = None, defaultValue: list = None):
        if not isinstance(accepted_types, (tuple, list)):
            self.accepted_types = [accepted_types]
        else:
            self.accepted_types = list(accepted_types)

        self._dict = defaultValue
        if defaultValue is None:
            self._dict = {}

    def save(self, name: str, object_):
        """
        Save object_ to the registry.
        """
        self._dict[name] = object

    def __iter__(self):
        self.iter_count = -1
        return self

    def __next__(self):
        self.iter_count += 1
        try:
            return self._dict[self.iter_count]
        except IndexError:
            raise StopIteration

    def __getitem__(self, item):
        return self._dict[item]


class Reflect:
    __slots__ = ['_target']

    def __init__(self, object_):
        self._target = object_

    def __call__(self, attr: str):
        return self._target.__getattribute__(attr)


class Iterable:
    TARGET_ATTR = []
    ITER_AMOUNT = 1
    ITER_START_VALUE = 0

    def __iter__(self):
        self.counter = self.ITER_START_VALUE - self.ITER_AMOUNT
        if isinstance(self.TARGET_ATTR, dict):
            self.relay_list = []
            for item in self.TARGET_ATTR:
                self.relay_list.append(item)

        return self

    def __next__(self):

        self.counter += self.ITER_AMOUNT
        if isinstance(self.TARGET_ATTR, dict):
            try:
                return self.relay_list[self.counter]
            except IndexError:
                raise StopIteration

        try:
            return self.TARGET_ATTR[self.counter]
        except IndexError:
            raise StopIteration

    @property
    def values(self):
        return self.TARGET_ATTR


class AbstractMethod:
    def __init__(self, func: FunctionType):
        self.func = func
        self.func.__qualname__ += "/abs"

    def _super_init_subclass(self):
        raise AttributeError('Abstract methods cannot be called!')

    def __call__(self, *args, **kwargs):
        raise AttributeError('Abstract methods cannot be called!')

