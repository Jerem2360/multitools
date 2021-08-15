from typing import Union


class ArithmeticSuite(object):
    def __init__(self, u0: Union[int, float], reason: Union[int, float]):
        self.u0 = float(u0)
        self.reason = float(reason)

    def __getitem__(self, item: int):
        return self.u0 + (self.reason * item)

    def to_list(self, limit: int):
        result = []
        for i in range(limit + 1):
            result.append(self[i])
        return result


class GeometricSuite(object):
    def __init__(self, u0: Union[int, float], reason: Union[int, float]):
        self.u0 = float(u0)
        self.reason = float(reason)

    def __getitem__(self, item: int):
        return self.u0 * (self.reason ** item)

    def to_list(self, limit: int):
        result = []
        for i in range(limit + 1):
            result.append(self[i])
        return result
