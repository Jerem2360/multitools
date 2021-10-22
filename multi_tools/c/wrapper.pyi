from . import types as _tp
from ctypes import c_int as _int
from _ctypes import CFuncPtr as _CFuncT
from types import FunctionType as _FuncT, MethodType as _MethT
from typing import Union as _Union, TypeVar as _TypeVar


_CData = _int.__bases__[0].__bases__[0]  # _ctypes._CData
_ArgMapping = dict[type[_tp.CObject], type[_CData]]
_RetMapping = dict[type[_CData], type[_tp.CObject]]
_Func = _Union[_FuncT, _MethT, _CFuncT]
_CValue = _TypeVar("_CValue", _tp.CObject, _CData)  # Union[CObject, _ctypes._CData]


def call_with_wrap(func: _Func, *args: _CValue, **kwargs: _CValue) -> _CValue: ...


class TypeWrap(object):

    argTypesMapping: _ArgMapping = ...
    retTypesMapping: _RetMapping = ...

    def __init__(self, func: _Func, *args: _CValue): ...

