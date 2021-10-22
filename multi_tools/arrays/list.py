class Table1D(object):
    def __init__(self, v: list):
        self._value = {}
        for i in v:
            self._value[i] = None

    def __getitem__(self, item):
        return self._value[item]

    def __setitem__(self, key: int, value):
        values = self.to_list()

        values[key] = value

        for w in values:
            self._value[w] = None

    def __delitem__(self, key: int):
        values = self.to_list()

        values.pop(key)

        self._value = []

        for w in values:
            self._value[w] = None

    def to_list(self):
        values = []
        for v in self._value:
            values.append(v)
        return values

    def __repr__(self): return repr(self.to_list())

    def __str__(self): return str(self.to_list())
