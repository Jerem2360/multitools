from multi_tools.errors import exceptions


class InfiniteDivisionError(exceptions.ErrorImitation):
    def __init__(self, text="Division by infinity", immediateRaise=True):
        exceptions.ErrorImitation.__init__(self, name="InfiniteDivisionError", text=text, immediateRaise=immediateRaise)
