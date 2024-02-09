

_valid_enum_types = str, int, float


class EnumerationType(type):
    def __new__(mcs, name, bases, np):
        enumtype = None
        for base in bases:
            if issubclass(base, _valid_enum_types):
                enumtype = base
                break
        if enumtype is None and len(bases):
            raise TypeError("Enum types must be " + " or ".join(tp.__name__ for tp in _valid_enum_types) + " types.")
        __elements__ = {}
        for name, value in np.copy().items():
            if isinstance(value, enumtype):
                __elements__[name] = np[value]
                del np[name]
        cls = type.__new__(mcs, name, bases, np)
        cls.__elements__ = __elements__
        cls.__enumtype__ = enumtype
        return cls

    def __getattr__(cls, item):
        try:
            return cls.__elements__[item]
        except KeyError:
            raise AttributeError(item) from None

