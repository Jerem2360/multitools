

class Group:
    def __init__(self, iter_amount, start_value=0):
        self.amount = iter_amount
        self.start_value = start_value

    def __iter__(self):
        self.num = self.start_value
        return self

    def __next__(self):
        result = self.num
        self.num += self.amount
        return result


class Reals(Group):
    def __init__(self):
        Group.__init__(self, 10 ** -323)


class Integers(Group):
    def __init__(self):
        Group.__init__(self, 1)
