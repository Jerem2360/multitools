

class _AnyMeta(type):
    def __instancecheck__(self, instance):
        return True


class Any(metaclass=_AnyMeta):
    def __init__(self):
        self._throw()

    def __init_subclass__(cls, **kwargs):
        cls._throw()

    @staticmethod
    def _throw():
        raise ValueError("'Any' cannot be instantiated nor subclassed.")


class _GenericMeta(type):
    def __new__(mcs, name, bases, np):
        cls = super().__new__(mcs, name, bases, np)
        cls.__generic_args__ = []
        return cls


class _GenericBuilderMeta(type):

    def __getitem__(cls, arg1: type, *genericargs) -> type:
        args = [arg1, *genericargs]

        cls.__check__(args)

        class GenericAlias(metaclass=_GenericMeta):

            __generic_args__ = [*args]

        return cls.__edit_type__(args, GenericAlias)

    def __check__(cls, args):
        pass

    def __edit_type__(cls, args, tp: type) -> type:
        return tp


class Generic(metaclass=_GenericBuilderMeta):

    pass
