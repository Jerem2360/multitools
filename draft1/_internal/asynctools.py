

class AsyncMapIterator:
    __slots__ = (
        '_map',
        '_n',
        '_owns',
    )

    def __init__(self, mapping):
        self._map = mapping
        self._n = 0

    def __next__(self):
        if self._n >= len(self._map):
            raise StopIteration
        res = self._map[self._n]
        self._n += 1
        return res


class AsyncMap(dict):
    """
    Thread-safe mapping.
    Threads must wait their turn to read or write data here.
    """

    __slots__ = (
        '_lock',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        import _thread
        self._lock = _thread.allocate_lock()

    def __getitem__(self, item):
        with self._lock:
            return super().__getitem__(item)

    def __setitem__(self, key, value):
        with self._lock:
            return super().__setitem__(key, value)

    def __delitem__(self, key):
        with self._lock:
            super().__delitem__(key)

    def __iter__(self):
        return AsyncMapIterator(self)

    def get(self, key, *args, **kwargs):
        if 'default' in kwargs:
            with self._lock:
                return super().get(key, kwargs['default'])
        if len(args):
            with self._lock:
                return super().get(key, args[0])
        with self._lock:
            return super().get(key)

    def copy(self):
        with self._lock:
            return AsyncMap(super().copy())



