from . import types
import ctypes
from ctypes import wintypes


class TypeWrap:

    @staticmethod
    def _common_name(name: str):
        key = getattr(wintypes, name)
        value = getattr(types.win32, name)
        return {key: value}

    @staticmethod
    def _reversed_common_name(name: str):
        key = getattr(types.win32, name)
        value = getattr(wintypes, name)
        return {key: value}

    @classmethod
    def _common_names(cls, *names: str):
        result = {**{cls._common_name(n) for n in names}}
        return result

    @classmethod
    def _reversed_common_names(cls, *names: str):
        result = {**{cls._reversed_common_name(n) for n in names}}
        return result

    argTypesMapping = {
        # standard C types:
        types.PyObject: ctypes.py_object,
        types.CShort: ctypes.c_short,
        types.CUShort: ctypes.c_ushort,
        types.CLong: ctypes.c_long,
        types.CULong: ctypes.c_ulong,
        types.CInt: ctypes.c_int,
        types.CUInt: ctypes.c_uint,
        types.CFloat: ctypes.c_float,
        types.CDouble: ctypes.c_double,
        types.CLongDouble: ctypes.c_longdouble,
        types.CLongLong: ctypes.c_longlong,
        types.CULongLong: ctypes.c_ulonglong,
        types.CByte: ctypes.c_byte,
        types.CUByte: ctypes.c_ubyte,
        types.CChar: ctypes.c_char,
        types.CCharPtr: ctypes.c_char_p,
        types.CVoidPtr: ctypes.c_void_p,
        types.CBool: ctypes.c_bool,
        types.CWchar: ctypes.c_wchar,
        types.CWcharPtr: ctypes.c_wchar_p,

        # Windows.h types:
        **_reversed_common_names(
            "BYTE", "WORD", "DWORD", "CHAR", "WCHAR", "INT", "UINT"
                                                             "FLOAT", "DOUBLE", "BOOLEAN", "BOOL", "VARIANT_BOOL",
            "LONG",
            "ULONG", "SHORT", "USHORT", "WPARAM", "LPARAM", "ATOM", "LANGID",
            "COLORREF", "LGRPID", "LCTYPE", "LCID", "HANDLE", "HACCEL", "HBITMAP",
            "HBRUSH", "HCOLORSPACE", "HDC", "HDESK", "HDWP", "HENHMETAFILE",
            "HFONT", "HGDIOBJ", "HGLOBAL", "HHOOK", "HICON", "HINSTANCE", "HKEY",
            "HKL", "HLOCAL", "HMENU", "HMETAFILE", "HMODULE", "HMONITOR",
            "HPALETTE", "HPEN", "HRGN", "HRSRC", "HSTR", "HTASK", "HWINSTA", "HWND",
            "SC_HANDLE", "SERVICE_STATUS_HANDLE", "LARGE_INTEGER", "ULARGE_INTEGER",
        ),

        # Windows.h structs:
        **_reversed_common_names(
            "RECT", "RECTL", "SMALL_RECT", "POINT", "POINTL", "SIZE", "SIZEL",
            "FILETIME", "MSG", "WIN32_FIND_DATAA", "WIN32_FIND_DATAW",
        ),
    }

    retTypesMapping = {
        # standard C types:
        ctypes.py_object: types.PyObject,
        ctypes.c_short: types.CShort,
        ctypes.c_ushort: types.CUShort,
        ctypes.c_long: types.CLong,
        ctypes.c_ulong: types.CULong,
        ctypes.c_int: types.CInt,
        ctypes.c_uint: types.CUInt,
        ctypes.c_float: types.CFloat,
        ctypes.c_double: types.CDouble,
        ctypes.c_longdouble: types.CLongDouble,
        ctypes.c_longlong: types.CLongLong,
        ctypes.c_ulonglong: types.CULongLong,
        ctypes.c_byte: types.CByte,
        ctypes.c_ubyte: types.CUByte,
        ctypes.c_char: types.CChar,
        ctypes.c_char_p: types.CCharPtr,
        ctypes.c_void_p: types.CVoidPtr,
        ctypes.c_bool: types.CBool,
        ctypes.c_wchar: types.CWchar,
        ctypes.c_wchar_p: types.CWcharPtr,

        # Windows.h types:
        **_common_names(
                        "BYTE", "WORD", "DWORD", "CHAR", "WCHAR", "INT", "UINT"
                        "FLOAT", "DOUBLE", "BOOLEAN", "BOOL", "VARIANT_BOOL", "LONG",
                        "ULONG", "SHORT", "USHORT", "WPARAM", "LPARAM", "ATOM", "LANGID",
                        "COLORREF", "LGRPID", "LCTYPE", "LCID", "HANDLE", "HACCEL", "HBITMAP",
                        "HBRUSH", "HCOLORSPACE", "HDC", "HDESK", "HDWP", "HENHMETAFILE",
                        "HFONT", "HGDIOBJ", "HGLOBAL", "HHOOK", "HICON", "HINSTANCE", "HKEY",
                        "HKL", "HLOCAL", "HMENU", "HMETAFILE", "HMODULE", "HMONITOR",
                        "HPALETTE", "HPEN", "HRGN", "HRSRC", "HSTR", "HTASK", "HWINSTA", "HWND",
                        "SC_HANDLE", "SERVICE_STATUS_HANDLE", "LARGE_INTEGER", "ULARGE_INTEGER",
                        ),

        # Windows.h structs:
        **_common_names(
                        "RECT", "RECTL", "SMALL_RECT", "POINT", "POINTL", "SIZE", "SIZEL",
                        "FILETIME", "MSG", "WIN32_FIND_DATAA", "WIN32_FIND_DATAW",
                        ),

    }

    def __init__(self, func, *args):
        """
        Internal helper for wrapping C function calls and returning to
        c.types.CObject subclass instances.
        """
        _args = []
        for arg in args:
            argtype = type(arg)
            if argtype in self.argTypesMapping:
                true_arg = arg.__origin__

            else:
                true_arg = arg
            _args.append(true_arg)

        result = func(*_args)
        if type(result) in self.retTypesMapping:
            restype = self.retTypesMapping[type(result)]
            res = restype(result)
        else:
            res = result

        self._retval = res

    ret = property(lambda self: self._retval)


def call_with_wrap(func, *args, **kwargs):
    """
    Call an external function as
    func(*args, *kwargs)
    and return it's result.

    Keyword arguments are converted to positional arguments and are
    added to the end of the standard positional arguments.
    """
    kwds = []
    for key in kwargs:
        kwds.append(kwargs.get(key))

    wrapped = TypeWrap(func, *args, *kwds)

    return wrapped.ret


