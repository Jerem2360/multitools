import typing

_TYPEERROR_PRECISE = "'{name}': Expected type '{expected}', got '{got}' instead."
_TYPEERROR = "Expected '{expected}', got '{got}' instead."


class _TypeCheckStatus:
    def __init__(self, expected=None, got=None):
        if None in (expected, got):
            self._expected = None
            self._got = None
        else:
            self._expected = expected
            self._got = got

    def __bool__(self):
        return None in (self._expected, self._got)

    def __and__(self, other):
        if not self:
            return _TypeCheckStatus(self._expected, self._got)
        return _TypeCheckStatus(other._expected, other._got)

    def format(self, **kwargs):
        if 'name' in kwargs:
            return _TYPEERROR_PRECISE.format(
                name=kwargs['name'],
                expected=self._expected,
                got=self._got
            )
        return _TYPEERROR.format(
            expected=self._expected,
            got=self._got
        )

    def exception(self, **kwargs):
        return TypeError(self.format(**kwargs))


def typecheck(*args, name=None, _raise=True):
    if len(args) % 2:
        raise TypeError("typecheck(): incorrect number of arguments.")

    sep = int(len(args) / 2)
    values = args[:sep]
    types = args[sep:]

    status = _TypeCheckStatus()
    for i in range(sep):
        status &= _check_arg(values[i], types[i])

    if not status:
        kwargs = {} if name is None else {'name': name}
        if _raise:
            raise status.exception(**kwargs)
        return status.format(**kwargs)
    return None


def _check_arg(value, tp, subclasscheck=False):
    import types
    print('type:', type(tp))

    try:
        iter(tp)
        _types = list(tp)
        union = _types.pop(0)
        for _tp in tp:
            union |= _tp
        tp = union
    except TypeError:
        pass

    if tp is None:
        return _check_arg(value, type(None))

    if isinstance(tp, types.GenericAlias):
        origin = tp.__origin__
        instance_check = _check_arg(value, origin)
        if not instance_check:
            return instance_check
        if origin is type:
            return _check_arg(value, tp.__args__[0], subclasscheck=True)
        if origin is list:
            for item in value:
                check_item = _check_arg(item, tp.__args__)
                if not check_item:
                    return check_item
        if origin is tuple:
            for i in range(len(tp.__args__)):
                arg, _tp = value[i], tp.__args__[i]
                check = _check_arg(arg, _tp)
                if not check:
                    return check
        if origin is set:
            for item in value:
                check = _check_arg(item, tp.__args__[0])
                if not check:
                    return check


        return _TypeCheckStatus()
    if isinstance(tp, types.UnionType):
        status = _TypeCheckStatus()
        for subtp in tp.__args__:
            status = _check_arg(value, subtp)
            if status:
                return status
        status._expected = repr(tp)
        return status

    if isinstance(tp, str):
        return _TypeCheckStatus()

    if subclasscheck:
        if issubclass(value, tp):  # type: ignore
            return _TypeCheckStatus()
        try:
            iter(tp)  # type: ignore
            fmt_tp = str(*(t.__name__ for t in tp)).replace('"', '')  # type: ignore
        except:
            fmt_tp = str([tp.__name__]).replace("'", "")
        return _TypeCheckStatus(f"type{fmt_tp}", type(value).__name__)

    if isinstance(value, tp):  # type: ignore
        return _TypeCheckStatus()

    try:
        iter(tp)  # type: ignore
        fmt_tp = ' | '.join(t.__name__ for t in tp)  # type: ignore
    except:
        fmt_tp = tp.__name__

    return _TypeCheckStatus(fmt_tp, type(value).__name__)

