import types
import inspect


__requires__ = (
    types.FunctionType,
    property,
)

import typing

_WrapperDescriptor = type(memoryview.__buffer__)


def _walk_bases(cls, base):
    if (cls is base) or (base in cls.__bases__):
        return True

    if object in cls.__bases__:
        return False

    for cls_base in cls.__bases__:
        if _walk_bases(cls_base, base):
            return True


class _ProtocolType(type):
    def __new__(mcs, name, bases, np):
        requires = {}

        bases = list(bases)
        if typing.Generic in bases:
            bases.pop(bases.index(typing.Generic))
        bases = tuple(bases)

        if len(bases):
            for aname, avalue in np.items():
                for req in __requires__:
                    if isinstance(avalue, req):
                        requires[aname] = req
                        break

            for base in bases:
                if not _walk_bases(base, Protocol):
                    raise TypeError("Protocols can only inherit from protocols.")
                requires = {**requires, **base._requires}

        cls = type.__new__(mcs, name, bases, np)
        cls._requires = requires
        return cls

    def __instancecheck__(cls, instance):
        return cls.__subclasscheck__(type(instance))

    def __subclasscheck__(cls, subclass):
        if cls.__base__ == object:
            return False
        # print(f"Checking: '{cls._requires}' ...")

        for name, tp in cls._requires.items():
            if not hasattr(subclass, name):
                # print(f"no attribute '{name}'")
                return False
            if tp in (types.FunctionType, classmethod, staticmethod):
                if not isinstance(getattr(subclass, name), (_WrapperDescriptor, types.FunctionType, classmethod, staticmethod)):
                    return False
                return _check_signature(cls, subclass, name, tp)

            if not isinstance(getattr(subclass, name), tp):
                # print("not the right type")
                # print(tp, type(getattr(subclass, name)))
                return False
            if not _check_signature(cls, subclass, name, tp):
                return False

        return True

    def __and__(cls, other) -> "type[Protocol]":

        return _ProtocolType(cls.__name__ + ' & ' + other.__name__, (cls, other), {})  # type: ignore

    def __repr__(cls):
        return f"<protocol '{cls.__name__}'>"


def _check_signature(protocol, checkcls, name, tp):
    """if not isinstance(getattr(checkcls, name, None), tp):
        return False"""
    if tp is property:
        return _check_property(protocol, checkcls, name)

    # print(f"Comparing signatures '{inspect.signature(getattr(protocol, name))}' and '{inspect.signature(getattr(checkcls, name))}'")

    f1 = getattr(protocol, name)
    f2 = getattr(checkcls, name)
    return _signature_compat(f1, f2) and _signature_compat(f2, f1)


def _check_property(protocol, checkcls, name):
    protocol_prop = getattr(protocol, name)
    checkcls_prop = getattr(checkcls, name)

    res = True
    if protocol_prop.fget:
        res &= (
            checkcls_prop.fget is not None and (
                inspect.signature(protocol_prop.fget) == inspect.signature(checkcls_prop.fget)
            )
        )
        # print(f"Compared signatures '{inspect.signature(protocol_prop.fget)}' and '{inspect.signature(checkcls_prop.fget)}' for property '{name}'.")
    if protocol_prop.fset:
        res &= (
            checkcls_prop.fset is not None and (
                inspect.signature(protocol_prop.fset) == inspect.signature(checkcls_prop.fset)
            )
        )
    if protocol_prop.fdel:
        res &= (
            checkcls_prop.fdel is not None and (
                inspect.signature(protocol_prop.fdel) == inspect.signature(checkcls_prop.fdel)
            )
        )
    return res



class Protocol(metaclass=_ProtocolType):
    """
    Actual implementation for the Protocol class.
    """
    def __new__(cls, *args, **kwargs):
        raise TypeError("Protocols cannot be instantiated.")

    def __class_getitem__(cls, item):
        return cls


def runtime_checkable(func=None, *args, **kwargs):
    return func


def _signature_compat(f1, f2):
    sig = inspect.signature(f1)
    sig2 = inspect.signature(f2)
    try:
        sig2.bind(*(None for p in sig.parameters.values() if p.kind != p.KEYWORD_ONLY))
    except TypeError:
        return False
    return True

