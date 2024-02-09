

def setattr(obj, name, value):
    """
    Set an object secret attribute's value.

    Secret attributes can only be accessed through the object's __dict__
    attribute with a decorated name or via this method. The standard '.'
    syntax cannot be used to access them.
    """
    import builtins
    return builtins.setattr(obj, '#' + name, value)


def getattr(obj, name):
    """
    Get an object secret attribute's value.
    See setattr() for details.
    """
    import builtins
    return builtins.getattr(obj, '#' + name)

