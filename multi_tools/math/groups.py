from typing import Literal


class Suite:
    def __init__(self, u0: float, n_max: int, r: float, operation: Literal['+'] or Literal['*']):
        self.value = u0
        self.u0 = u0
        self.n_max = n_max
        self.operator = operation
        self.reason = r
        self.n = 0

    def __iter__(self):
        return self

    def __next__(self):
        result = self.value
        if self.n <= self.n_max:
            self.n += 1
            self.value = eval(f"{self.value} {self.operator} {self.reason}")
            print(f"(__next__) {result}")
            return result
        raise StopIteration

    def __repr__(self):
        return f"<Suite object at {id(self)}, r={self.reason}, n={self.n_max}, U0={self.u0}, type=\"{self.operator}\">"

    def __getitem__(self, item: int):
        items = []
        for item_ in self:
            items.append(item_)

        return items[item]
