import ctypes
import _ctypes
from ctypes import wintypes


def check_size(typ, typecode=None):
    from struct import calcsize
    if typecode is None:
        typecode = typ.__tpid__
    actual, required = typ.__tpsize__, calcsize(typecode)
    del calcsize
    if actual != required:
        raise SystemError("Size of C type '%s' wrong: %d instead of %d" % (typ.__typename__, actual, required))


CData = ctypes.Structure.__bases__[0]
SimpleCData = _ctypes._SimpleCData
NoneType = type(None)


def isoftype(obj, tp) -> bool:
    return type(obj) == tp


def issubinstance(obj, tp) -> bool:
    return tp in type(obj).__bases__


def meta_default_classattr(cls, attr_name, default_value):
    if not hasattr(cls, attr_name):
        cls.__setattr__(attr_name, default_value)
    return cls


sizeof = _ctypes.sizeof

# c type ids:
PY_OBJECT: str = "py_object"
C_SHORT: str = "c_short"
C_USHORT: str = "c_ushort"
C_LONG: str = "c_long"
C_ULONG: str = "c_ulong"
C_INT: str = "c_int"
C_UINT: str = "c_uint"
C_FLOAT: str = "c_float"
C_DOUBLE: str = "c_double"
C_LONGDOUBLE: str = "c_longdouble"
C_LONGLONG: str = "c_longlong"
C_ULONGLONG: str = "c_ulonglong"
C_UBYTE: str = "c_ubyte"
C_BYTE: str = "c_byte"
C_CHAR: str = "c_char"
C_CHAR_P: str = "c_char_p"
C_VOID_P: str = "c_void_p"
C_BOOL: str = "c_bool"
C_WCHAR_P: str = "c_wchar_p"
C_WCHAR: str = "c_wchar"
WIN_SPEC_VAR_BOOL: str = "win_special_variant_bool"


def size_and_name(ctyp, name):
    return sizeof(ctyp), name


TYPE_INFO = {
    "py_object": size_and_name(ctypes.py_object, "O"),
    "c_short": size_and_name(ctypes.c_short, "h"),
    "c_ushort": size_and_name(ctypes.c_ushort, "H"),
    "c_long": size_and_name(ctypes.c_long, "l"),
    "c_ulong": size_and_name(ctypes.c_ulong, "L"),
    "c_int": size_and_name(ctypes.c_int, "i"),
    "c_uint": size_and_name(ctypes.c_uint, "I"),
    "c_float": size_and_name(ctypes.c_float, "f"),
    "c_double": size_and_name(ctypes.c_double, "d"),
    "c_longdouble": size_and_name(ctypes.c_longdouble, "g"),
    "c_longlong": size_and_name(ctypes.c_longlong, "q"),
    "c_ulonglong": size_and_name(ctypes.c_ulonglong, "Q"),
    "c_ubyte": size_and_name(ctypes.c_ubyte, "B"),
    "c_byte": size_and_name(ctypes.c_byte, "b"),
    "c_char": size_and_name(ctypes.c_char, "c"),
    "c_char_p": size_and_name(ctypes.c_char_p, "z"),
    "c_void_p": size_and_name(ctypes.c_void_p, "p"),
    "c_bool": size_and_name(ctypes.c_bool, "?"),
    "c_wchar_p": size_and_name(ctypes.c_wchar_p, "z"),
    "c_wchar": size_and_name(ctypes.c_wchar, "u"),

    "win_special_variant_bool": size_and_name(wintypes.VARIANT_BOOL, "v"),
}

