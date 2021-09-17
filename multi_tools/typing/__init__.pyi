

class GenericInstance(object):

    __generic_args__: list[type]

    def __init__(self, *args, **kwargs): ...


class Generic(object):
    """
    Base class for simple generic types. See typing.Generic (python builtin module) for more advanced
    Generic types.

    To create a simple generic type, make it inheritate from Generic.
    """

    @classmethod
    def __check__(cls, args: list[type]):
        """
        Override this for custom generic argument checking.
        """
        pass

    @classmethod
    def __edit_type__(cls, args: list[type], tp: type[GenericInstance]) -> type[GenericInstance]:
        """
        Override this to customize generic instances.
        """
        pass

    def __class_getitem__(cls, *items: type) -> GenericInstance: ...


class Any:
    pass


