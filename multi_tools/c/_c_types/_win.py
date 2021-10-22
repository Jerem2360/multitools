from ._base_types import *


def POINTER(tp: type[CObject]) -> type[ctypes.pointer]:
    return ctypes.POINTER(tp.__origin__)


class BYTE(CByte):
    __tprepr__ = "Windows.BYTE"


class WORD(CUShort):
    __tprepr__ = "Windows.WORD"


class DWORD(CULong):
    __tprepr__ = "Windows.DWORD"


class CHAR(CChar):
    __tprepr__ = "Windows.CHAR"


class WCHAR(CWchar):
    __tprepr__ = "Windows.WCHAR"


class UINT(CUInt):
    __tprepr__ = "Windows.UINT"


class INT(CInt):
    __tprepr__ = "Windows.INT"


class DOUBLE(CDouble):
    __tprepr__ = "Windows.DOUBLE"


class FLOAT(CFloat):
    __tprepr__ = "Windows.FLOAT"


class BOOLEAN(BYTE):
    __tprepr__ = "Windows.BOOLEAN"


class BOOL(CLong):
    __tprepr__ = "Windows.BOOL"


class VARIANT_BOOL(CObject):
    __tpid__ = "v"
    __typename__ = WIN_SPEC_VAR_BOOL
    __tprepr__ = "Windows.VARIANT_BOOL"


class ULONG(CULong):
    __tprepr__ = "Windows.ULONG"


class LONG(CLong):
    __tprepr__ = "Windows.LONG"


class USHORT(CUShort):
    __tprepr__ = "Windows.USHORT"


class SHORT(CShort):
    __tprepr__ = "Windows.SHORT"


if ctypes.sizeof(ctypes.c_long) == ctypes.sizeof(ctypes.c_void_p):
    _WPARAM = CULong
    _LPARAM = CLong
elif ctypes.sizeof(ctypes.c_longlong) == ctypes.sizeof(ctypes.c_void_p):
    _WPARAM = CULongLong
    _LPARAM = CLongLong
else:
    _WPARAM = CULong
    _LPARAM = CLong


class WPARAM(_WPARAM):
    __tprepr__ = "Windows.WPARAM"


class LPARAM(_LPARAM):
    __tprepr__ = "Windows.LPARAM"


class ATOM(WORD):
    __tprepr__ = "Windows.ATOM"


class LANGID(WORD):
    __tprepr__ = "Windows.LANGID"


class COLORREF(DWORD):
    __tprepr__ = "Windows.COLORREF"


class LGRPID(DWORD):
    __tprepr__ = "Windows.LGRPID"


class LCTYPE(DWORD):
    __tprepr__ = "Windows.LCTYPE"


class LCID(DWORD):
    __tprepr__ = "Windows.LCID"


class HANDLE(CVoidPtr):
    __tprepr__ = "Windows.HANDLE"


class HACCEL(HANDLE):
    __tprepr__ = "Windows.HACCEL"


class HBITMAP(HANDLE):
    __tprepr__ = "Windows.HBITMAP"


class HBRUSH(HANDLE):
    __tprepr__ = "Windows.HBRUSH"


class HCOLORSPACE(HANDLE):
    __tprepr__ = "Windows.HCOLORSPACE"


class HDC(HANDLE):
    __tprepr__ = "Windows.HDC"


class HDESK(HANDLE):
    __tprepr__ = "Windows.HDESK"


class HDWP(HANDLE):
    __tprepr__ = "Windows.HDWP"


class HENHMETAFILE(HANDLE):
    __tprepr__ = "Windows.HENHMETAFILE"


class HFONT(HANDLE):
    __tprepr__ = "Windows.HFONT"


class HGDIOBJ(HANDLE):
    __tprepr__ = "Windows.HGDIOBJ"


class HGLOBAL(HANDLE):
    __tprepr__ = "Windows.HGLOBAL"


class HHOOK(HANDLE):
    __tprepr__ = "Windows.HHOOK"


class HICON(HANDLE):
    __tprepr__ = "Windows.HICON"


class HINSTANCE(HANDLE):
    __tprepr__ = "Windows.HINSTANCE"


class HKEY(HANDLE):
    __tprepr__ = "Windows.HKEY"


class HKL(HANDLE):
    __tprepr__ = "Windows.HKL"


class HLOCAL(HANDLE):
    __tprepr__ = "Windows.HLOCAL"


class HMENU(HANDLE):
    __tprepr__ = "Windows.HMENU"


class HMETAFILE(HANDLE):
    __tprepr__ = "Windows.HMETAFILE"


class HMODULE(HANDLE):
    __tprepr__ = "Windows.HMODULE"


class HMONITOR(HANDLE):
    __tprepr__ = "Windows.HMONITOR"


class HPALETTE(HANDLE):
    __tprepr__ = "Windows.HPALETTE"


class HPEN(HANDLE):
    __tprepr__ = "Windows.HPEN"


class HRGN(HANDLE):
    __tprepr__ = "Windows.HRGN"


class HRSRC(HANDLE):
    __tprepr__ = "Windows.HRSRC"


class HSTR(HANDLE):
    __tprepr__ = "Windows.HSTR"


class HTASK(HANDLE):
    __tprepr__ = "Windows.HTASK"


class HWINSTA(HANDLE):
    __tprepr__ = "Windows.HWINSTA"


class HWND(HANDLE):
    __tprepr__ = "Windows.HWND"


class SC_HANDLE(HANDLE):
    __tprepr__ = "Windows.SC_HANDLE"


class SERVICE_STATUS_HANDLE(HANDLE):
    __tprepr__ = "Windows.SERVICE_STATUS_HANDLE"


class LARGE_INTEGER(CLongLong):
    __tprepr__ = "Windows.LARGE_INTEGER"


class ULARGE_INTEGER(CULongLong):
    __tprepr__ = "Windows.ULARGE_INTEGER"


# structs:

class RECT(CStruct):
    __fields__ = [
        ("left", LONG),
        ("right", LONG),
        ("top", LONG),
        ("bottom", LONG),
    ]

    __tprepr__ = "Windows.RECT"


RECTL = RECT


class SMALL_RECT(CStruct):
    __fields__ = [
        ("Left", SHORT),
        ("Right", SHORT),
        ("Top", SHORT),
        ("Bottom", SHORT),
    ]

    __tprepr__ = "Windows.SMALL_RECT"


class _COORD(CStruct):
    __fields__ = [
        ("X", SHORT),
        ("Y", SHORT),
    ]

    __tprepr__ = "Windows._COORD"


class POINT(CStruct):
    __fields__ = [
        ("x", LONG),
        ("y", LONG),
    ]

    __tprepr__ = "Windows.POINT"

POINTL = POINT


class SIZE(CStruct):
    __fields__ = [
        ("cx", LONG),
        ("cy", LONG),
    ]

    __tprepr__ = "Windows.SIZE"


SIZEL = SIZE


class FILETIME(CStruct):
    __fields__ = [
        ("dwLowDateTime", DWORD),
        ("dwHighDateTime", DWORD),
    ]
    __tprepr__ = "Windows.FILETIME"


class MSG(CStruct):
    __fields__ = [
        ("hWnd", HWND),
        ("message", UINT),
        ("wParam", WPARAM),
        ("lParam", LPARAM),
        ("time", DWORD),
        ("pt", POINT),
    ]

    __tprepr__ = "Windows.MSG"


class WIN32_FIND_DATAA(CStruct):
    __fields__ = [
        ("dwFileAttributes", DWORD),
        ("ftCreationTime", FILETIME),
        ("ftLastAccessTime", FILETIME),
        ("ftLastWriteTime", FILETIME),
        ("nFileSizeHigh", DWORD),
        ("nFileSizeLow", DWORD),
        ("dwReserved0", DWORD),
        ("dwReserved1", DWORD),
        ("cFileName", CChar[260]),
        ("cAlternateFileName", CChar[14]),
    ]

    __tprepr__ = "Windows.WIN32_FIND_DATAA"


class WIN32_FIND_DATAW(CStruct):
    __fields__ = [
        ("dwFileAttributes", DWORD),
        ("ftCreationTime", FILETIME),
        ("ftLastAccessTime", FILETIME),
        ("ftLastWriteTime", FILETIME),
        ("nFileSizeHigh", DWORD),
        ("nFileSizeLow", DWORD),
        ("dwReserved0", DWORD),
        ("dwReserved1", DWORD),
        ("cFileName", CChar[260]),
        ("cAlternateFileName", CChar[14]),
    ]

    __tprepr__ = "Windows.WIN32_FIND_DATAW"


LPBOOL = PBOOL = POINTER(BOOL)
PBOOLEAN = POINTER(BOOLEAN)
LPBYTE = PBYTE = POINTER(BYTE)
PCHAR = POINTER(CHAR)
LPCOLORREF = POINTER(COLORREF)
LPDWORD = PDWORD = POINTER(DWORD)
LPFILETIME = PFILETIME = POINTER(FILETIME)
PFLOAT = POINTER(FLOAT)
LPHANDLE = PHANDLE = POINTER(HANDLE)
PHKEY = POINTER(HKEY)
LPHKL = POINTER(HKL)
LPINT = PINT = POINTER(INT)
PLARGE_INTEGER = POINTER(LARGE_INTEGER)
PLCID = POINTER(LCID)
LPLONG = PLONG = POINTER(LONG)
LPMSG = PMSG = POINTER(MSG)
LPPOINT = PPOINT = POINTER(POINT)
PPOINTL = POINTER(POINTL)
LPRECT = PRECT = POINTER(RECT)
LPRECTL = PRECTL = POINTER(RECTL)
LPSC_HANDLE = POINTER(SC_HANDLE)
PSHORT = POINTER(SHORT)
LPSIZE = PSIZE = POINTER(SIZE)
LPSIZEL = PSIZEL = POINTER(SIZEL)
PSMALL_RECT = POINTER(SMALL_RECT)
LPUINT = PUINT = POINTER(UINT)
PULARGE_INTEGER = POINTER(ULARGE_INTEGER)
PULONG = POINTER(ULONG)
PUSHORT = POINTER(USHORT)
PWCHAR = POINTER(WCHAR)
LPWIN32_FIND_DATAA = PWIN32_FIND_DATAA = POINTER(WIN32_FIND_DATAA)
LPWIN32_FIND_DATAW = PWIN32_FIND_DATAW = POINTER(WIN32_FIND_DATAW)
LPWORD = PWORD = POINTER(WORD)

