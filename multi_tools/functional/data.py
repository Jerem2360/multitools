

def copy_func_data(source_func, dest_func):
    """
    Copy all useful data that is not the __code__ from source to
    destination and return destination.
    """
    dest_func.__name__ = source_func.__name__
    dest_func.__qualname__ = source_func.__qualname__
    dest_func.__doc__ = source_func.__doc__
    dest_func.__annotations__ = source_func.__annotations__
    dest_func.__defaults__ = source_func.__defaults__
    dest_func.__module__ = source_func.__module__
    dest_func.__kwdefaults__ = source_func.__kwdefaults__
    return dest_func
