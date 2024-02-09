import random

prefix = '#multitools' + hex(random.randint(0, 0xffff)).removeprefix('0x').zfill(4) + '@'


def setattr(obj, name, value):
    """
    Set an object secret attribute's value.

    Secret attributes can only be accessed through the object's __dict__
    attribute with a decorated name or via this method. The standard '.'
    syntax cannot be used to access them.
    """
    import builtins
    return builtins.setattr(obj, prefix + name, value)


def getattr(obj, name):
    """
    Get an object secret attribute's value.
    See setattr() for details.
    """
    import builtins
    return builtins.getattr(obj, prefix + name)

