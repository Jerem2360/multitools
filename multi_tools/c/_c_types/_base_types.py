from ._const import *
from typing import TypeVar
import ctypes


# a wrapper for our CObject class to handle _ctypes._SimpleCData and it's _type_ attribute.
def _SimpleCDataWrapper(t_: str = "O") -> type:
    class _Wrap(SimpleCData):
        _type_ = t_

        def __sup__(self, *args, **kwargs):
            return super(*args, **kwargs)

    return _Wrap


def _CObjectFromCData(data: CData) -> tuple[type, str]:
    tp = type(data)
    if not issubclass(tp, CData):
        return NoneType
    tpid = data._type_
    return _SimpleCDataWrapper(tpid), tpid


# metaclass for our CObject class and it's __typename__ property.
class _CObjectMeta(type):
    __slots__ = ["__tprepr__", "_tpname", "__tpid__", "__tpsize__", "__tporigin__"]

    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(*args, **kwargs)
        cls = meta_default_classattr(cls, "__tprepr__", "Object")
        cls = meta_default_classattr(cls, "_tpname", PY_OBJECT)
        cls = meta_default_classattr(cls, "__tpid__", TYPE_INFO[PY_OBJECT][1])
        cls = meta_default_classattr(cls, "__tpsize__", TYPE_INFO[PY_OBJECT][0])
        cls = meta_default_classattr(cls, "__tporigin__", ctypes.py_object)
        return cls

    def __init__(cls, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @property
    def __typename__(cls):
        return cls._tpname

    @__typename__.setter
    def __typename__(cls, value):
        tpsize, tpid = TYPE_INFO[value]
        cls.__tpid__ = tpid
        cls.__tpsize__ = tpsize
        cls._tpname = value


_T = TypeVar("_T")


class CObject(object, metaclass=_CObjectMeta):
    __ctype_be__ = None
    __ctype_le__ = None
    __tporigin__ = ctypes.py_object

    __slots__ = ["_data", "__origin__"]

    def __init_subclass__(cls, **kwargs):
        cls.__metaclass__ = _CObjectMeta
        cls.__init_subclass__ = CObject.__init_subclass__

    def __init__(self, value):
        self.__origin__ = value
        if issubinstance(value, CData):  # to replace with more cleaner function.
            data_type, tpid = _CObjectFromCData(value)
            if not (tpid == self.__tpid__):
                raise TypeError(f"Expected python equivalent for '{self.__class__.__name__}', "
                                f"got '{type(value)}' instead.")
            value = value.value
        else:
            data_type = _SimpleCDataWrapper(self.__tpid__)
        if self.__ctype_be__ is not None:
            data_type.__ctype_be__ = self.__ctype_be__
        if self.__ctype_le__ is not None:
            data_type.__ctype_le__ = self.__ctype_le__
        self._data = data_type(value)
        self._data.__repr__ = self.__repr__

        type(self).__origin__ = data_type
        # _SimpleCDataWrapper(c_api_type_indicator)(CData_value)

    def __repr__(self):
        return f"<C '{self.__tprepr__}' object at 0x{str(hex(id(self))).removeprefix('0x').upper()}>"

    @property
    def value(self):
        return self._data.value

    @value.setter
    def value(self, __v):
        self._data.value = __v

    def super(self, *args, **kwargs):
        return self._data.__sup__(*args, **kwargs)

    CData = property(lambda self: self._data)


class CObjectPtr(CObject):
    def __init__(self, value: ctypes.pointer):
        super().__init__(value)

    def __repr__(self):
        void_p = ctypes.cast(self._data, ctypes.c_void_p)
        addr = ctypes.cast(void_p, ctypes.c_int)
        return f"<Pointer to {addr.value} at 0x{str(hex(id(self))).removeprefix('0x').upper()}>"


class _StructMeta(type):
    __slots__ = ["_handle"]

    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        return cls

    def __repr__(cls):
        return f"<C struct '{cls.__name__}'>"

    @property
    def __tporigin__(cls):
        return cls._handle


class CStruct(CObject):
    __fields__ = []

    def __new__(cls, *args, **kwargs):
        buffer = cls.__repr__
        cls.__repr__ = lambda s: cls._handle.__repr__()
        if buffer == CStruct.__repr__:
            buffer = None
        ctypesStruct = cls._BuildCtypesStructure()
        self = super().__new__()
        self._handle = ctypesStruct(*args, **kwargs)
        if buffer is not None:
            self._handle.__repr__ = buffer
        return self

    def __init__(self, *args, **kwargs):
        self._handle.__init__(*args, **kwargs)
        super().__init__(self._handle)

    @classmethod
    def _BuildCtypesStructure(cls):
        class Struct(ctypes.Structure):
            _fields_ = cls._ConvertFields()

        return Struct

    @classmethod
    def _ConvertFields(cls) -> list[tuple[str, CData]]:
        result = []
        for field in cls.__fields__:
            name, tp = field
            new_tp = tp.__origin__
            result.append((name, new_tp))

        return result

    def __getattr__(self, item):
        if item == "__init__":
            raise TypeError("Structs don't have constructors.")
        return super().__getattribute__(item)

    def __repr__(self):
        return self._handle.__repr__()


class PyObject(CObject):
    __typename__ = PY_OBJECT
    __tprepr__ = "PyObject*"
    __tporigin__ = ctypes.py_object

    def __repr__(self):
        try:
            return super().__repr__()
        except ValueError:
            return "%s(<NULL>)" % type(self.CData).__name__


check_size(PyObject, "P")


class CShort(CObject):
    __typename__ = C_SHORT
    __tprepr__ = "short"
    __tporigin__ = ctypes.c_short


check_size(CShort)


class CUShort(CObject):
    __typename__ = C_USHORT
    __tprepr__ = "unsigned short"
    __tporigin__ = ctypes.c_ushort


check_size(CUShort)


class CLong(CObject):
    __typename__ = C_LONG
    __tprepr__ = "long"
    __tporigin__ = ctypes.c_long


check_size(CLong)


class CULong(CObject):
    __typename__ = C_ULONG
    __tprepr__ = "unsigned long"
    __tporigin__ = ctypes.c_ulong


check_size(CULong)


class CInt(CObject):
    __typename__ = C_INT
    __tprepr__ = "int"
    __tporigin__ = ctypes.c_int


check_size(CInt)


class CUInt(CObject):
    __typename__ = C_UINT
    __tprepr__ = "unsigned int"
    __tporigin__ = ctypes.c_uint


check_size(CUInt)

from struct import calcsize

if calcsize("i") == calcsize("l"):
    CInt = CLong
    CUInt = CULong
del calcsize


class CFloat(CObject):
    __typename__ = C_FLOAT
    __tprepr__ = "float"
    __tporigin__ = ctypes.c_float


check_size(CFloat)


class CDouble(CObject):
    __typename__ = C_DOUBLE
    __tprepr__ = "double"
    __tporigin__ = ctypes.c_double


check_size(CDouble)


class CLongDouble(CObject):
    __typename__ = C_LONGDOUBLE
    __tprepr__ = "long double"
    __tporigin__ = ctypes.c_longdouble


check_size(CLongDouble)


class CLongLong(CObject):
    __typename__ = C_LONGLONG
    __tprepr__ = "long long"
    __tporigin__ = ctypes.c_longlong


check_size(CLongLong)


class CULongLong(CObject):
    __typename__ = C_ULONGLONG
    __tprepr__ = "unsigned long long"
    __tporigin__ = ctypes.c_ulonglong


from struct import calcsize

if calcsize("l") == calcsize("q"):
    CLongLong = CLong
    CULongLong = CULong
del calcsize


class CByte(CObject):
    __typename__ = C_BYTE
    __tprepr__ = "char[] (bytes)"
    __tporigin__ = ctypes.c_byte


CByte.__ctype_le__ = CByte.__ctype_be__ = ctypes.c_byte
check_size(CByte)


class CUByte(CObject):
    __typename__ = C_UBYTE
    __tprepr__ = "unsigned char[] (bytes)"
    __tporigin__ = ctypes.c_ubyte


CUByte.__ctype_le__ = CUByte.__ctype_be__ = ctypes.c_ubyte
check_size(CUByte)


class CChar(CObject):
    __typename__ = C_CHAR
    __tprepr__ = "char"
    __tporigin__ = ctypes.c_char

    def __class_getitem__(cls, item: int):
        return ctypes.c_char * item


CChar.__ctype_le__ = CChar.__ctype_be__ = ctypes.c_char
check_size(CChar)


class CCharPtr(CObject):
    __typename__ = C_CHAR_P
    __tprepr__ = "char* || char[]"
    __tporigin__ = ctypes.c_char_p

    def lookup(self):
        return ctypes.c_void_p.from_buffer(self._data).value


check_size(CCharPtr, "P")


class CVoidPtr(CObject):
    __typename__ = C_VOID_P
    __tprepr__ = "void*"
    __tporigin__ = ctypes.c_void_p

    def lookup(self):
        return ctypes.c_void_p.from_buffer(self._data)


check_size(CVoidPtr)


class CBool(CObject):
    __typename__ = C_BOOL
    __tprepr__ = "bool"
    __tporigin__ = ctypes.c_bool


class CWchar(CObject):
    __typename__ = C_WCHAR
    __tprepr__ = "wchar"
    __tporigin__ = ctypes.c_wchar


class CWcharPtr(CObject):
    __typename__ = C_WCHAR_P
    __tprepr__ = "wchar* || wchar[]"
    __tporigin__ = ctypes.c_wchar_p

    def lookup(self):
        return ctypes.c_void_p.from_buffer(self._data).value

