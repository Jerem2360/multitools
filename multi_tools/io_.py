from sys import stdout, stdin


class ostream:
    def __init__(self):
        self.out = stdout

    def write(self, text):
        self.out.write(text)

    def __repr__(self):
        return f"<TextIO at {id(self)}, type=O>"


class istream:
    def __init__(self):
        self.out = stdin

    def write(self, text):
        self.out.write(text)

    def __repr__(self):
        return f"<TextIO at {id(self)}, type=I>"
