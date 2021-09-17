

class _GenericBuilderMeta(type):

    def __getitem__(cls, arg1: type, *genericargs):
        args = list((arg1, *genericargs))

        class GenericAlias(object):

            __generic_args__ = args

        return GenericAlias


class Generic(metaclass=_GenericBuilderMeta):

    pass

