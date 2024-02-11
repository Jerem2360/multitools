import random

prefix = '#multitools' + hex(random.randint(0, 0xffff)).removeprefix('0x').zfill(4) + '@'


def setattr(obj, name, value):
    """
    Set an object secret attribute's value.

    Secret attributes can only be accessed through the object's __dict__
    attribute with a decorated name or via this method. The standard '.'
    syntax cannot be used to access them.
    Note that secret attribute names can be the empty string.
    However, they must satisfy the str.isidentifier() condition.
    """
    import builtins
    if not (str(name).isidentifier() or str(name) == ''):
        raise NameError("Secret attribute names must satisfy the identifier format.")
    return builtins.setattr(obj, prefix + name, value)


def getattr(obj, name):
    """
    Get an object secret attribute's value.
    See setattr() for details.
    """
    import builtins
    return builtins.getattr(obj, prefix + name)


def dir(obj):
    """
    Return a list of the object's secret attribute names.
    """
    return list(n.removeprefix(prefix) for n in object.__dir__(obj) if n.startswith(prefix))

