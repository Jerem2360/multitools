from typing import Literal


def format_id(obj):
    hex_ = hex(id(obj))
    inter = str(hex_).split('0x')[-1].upper()
    return '0x' + inter


def typename(obj):
    """
    Get the string name of a type.
    """
    return eval("type(obj).__name__", {'obj': obj, **globals()}, locals())


class GeometryObject(object):
    """
    An empty common base for all geometry objects.
    """
    pass



