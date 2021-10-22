from typing import Union


class Formula(object):
    def __init__(self, formula: str, unknowns: tuple[str]):
        self._formula: str = formula
        self._u = unknowns

        x = {}
        for u in unknowns:
            x[u] = None

    def replace_letter(self, letter: str, value: Union[int, float]):
        result = self._formula.replace(letter, str(value))
        u = list(self._u)
        u.pop()
        return Formula(result, self._u)



