from typing import Any


class Registry:
    """
    A type representing a registry.
    """
    def __init__(self, accepted_types: type or tuple[type] = None, defaultValue: list = None):
        if not isinstance(accepted_types, (tuple, list)):
            self.accepted_types = [accepted_types]
        else:
            self.accepted_types = list(accepted_types)

        self.list = defaultValue
        if defaultValue is None:
            self.list = []

    def save(self, object_):
        """
        Save object_ to the registry.
        """
        self.list.append(object_)

    def __iter__(self):
        self.iter_count = -1
        return self

    def __next__(self):
        self.iter_count += 1
        try:
            return self.list[self.iter_count]
        except IndexError:
            raise StopIteration


class Reflect:
    def __init__(self, object_):
        self._target = object_

    def __call__(self, attr: str):
        return self._target.__getattribute__(attr)

