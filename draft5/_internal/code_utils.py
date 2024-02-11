

def _try_args(func, *args, **kwargs):
    import inspect
    if not callable(func):
        return False
    sig = inspect.signature(func)
    try:
        sig.bind(*args, **kwargs)
    except TypeError:
        return False
    return True


def _copy_code(
        codeobj, *,
        argcount: int = ...,
        posonlyargcount: int = ...,
        kwonlyargcount: int = ...,
        nlocals: int = ...,
        stacksize: int = ...,
        flags: int = ...,
        code: bytes = ...,
        consts: tuple[object, ...] = ...,
        names: tuple[str, ...] = ...,
        varnames: tuple[str, ...] = ...,
        filename: str = ...,
        name: str = ...,
        qualname: str = ...,
        firstlineno: int = ...,
        linetable: bytes = ...,
        exceptiontable: bytes = ...,
        freevars: tuple[str, ...] = ...,
        cellvars: tuple[str, ...] = ...,
        ):
    import types
    import sys

    if argcount is ...:
        argcount = codeobj.co_argcount
    if posonlyargcount is ...:
        posonlyargcount = codeobj.co_posonlyargcount
    if kwonlyargcount is ...:
        kwonlyargcount = codeobj.co_kwonlyargcount
    if nlocals is ...:
        nlocals = codeobj.co_nlocals
    if stacksize is ...:
        stacksize = codeobj.co_stacksize
    if flags is ...:
        flags = codeobj.co_flags
    if code is ...:
        code = codeobj.co_code
    if consts is ...:
        consts = codeobj.co_consts
    if names is ...:
        names = codeobj.co_names
    if varnames is ...:
        varnames = codeobj.co_varnames
    if filename is ...:
        filename = codeobj.co_filename
    if name is ...:
        name = codeobj.co_name

    if sys.version_info >= (3, 11):
        if qualname is ...:
            qualname = codeobj.co_qualname
        if exceptiontable is ...:
            exceptiontable = codeobj.co_exceptiontable

    if firstlineno is ...:
        firstlineno = codeobj.co_firstlineno

    if sys.version_info >= (3, 10):
        if linetable is ...:
            linetable = codeobj.co_linetable

    if freevars is ...:
        freevars = codeobj.co_freevars
    if cellvars is ...:
        cellvars = codeobj.co_cellvars


    if sys.version_info >= (3, 11):
        return types.CodeType(
            argcount,
            posonlyargcount,
            kwonlyargcount,
            nlocals,
            stacksize,
            flags,
            code,
            consts,
            names,
            varnames,
            filename,
            name,
            qualname,
            firstlineno,
            linetable,
            exceptiontable,
            freevars,
            cellvars
        )
    if sys.version_info >= (3, 10):
        return types.CodeType(
            argcount,
            posonlyargcount,
            kwonlyargcount,
            nlocals,
            stacksize,
            flags,
            code,
            consts,
            names,
            varnames,
            filename,
            name,
            firstlineno,
            linetable,
            freevars,
            cellvars
        )

    return types.CodeType(
        argcount,
        posonlyargcount,
        kwonlyargcount,
        nlocals,
        stacksize,
        flags,
        code,
        consts,
        names,
        varnames,
        filename,
        name,
        firstlineno,
        linetable,
        freevars,
        cellvars
    )




