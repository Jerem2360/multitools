from . import _c_types as _ct


"""Constants"""


# types' representation strings:

PY_OBJECT = _ct.PY_OBJECT
C_SHORT = _ct.C_SHORT
C_USHORT = _ct.C_USHORT
C_LONG = _ct.C_LONG
C_ULONG = _ct.C_ULONG
C_INT = _ct.C_INT
C_UINT = _ct.C_UINT
C_FLOAT = _ct.C_FLOAT
C_DOUBLE = _ct.C_DOUBLE
C_LONGDOUBLE = _ct.C_LONGDOUBLE
C_LONGLONG = _ct.C_LONGLONG
C_ULONGLONG = _ct.C_ULONGLONG
C_BYTE = _ct.C_BYTE
C_UBYTE = _ct.C_UBYTE
C_CHAR = _ct.C_CHAR
C_CHAR_PTR = _ct.C_CHAR_P
C_VOID_PTR = _ct.C_VOID_P
C_BOOL = _ct.C_BOOL
C_WCHAR = _ct.C_WCHAR
C_WCHAR_PTR = _ct.C_WCHAR_P


# Type info database (display name and size in memory):

TYPE_INFO = _ct.TYPE_INFO


# C types


CObject = _ct.CObject
CStruct = _ct.CStruct
PyObject = _ct.PyObject
CShort = _ct.CShort
CUShort = _ct.CUShort
CLong = _ct.CLong
CULong = _ct.CULong
CInt = _ct.CInt
CUInt = _ct.CUInt
CFloat = _ct.CFloat
CDouble = _ct.CDouble
CLongDouble = _ct.CLongDouble
CLongLong = _ct.CLongLong
CULongLong = _ct.CULongLong
CByte = _ct.CByte
CUByte = _ct.CUByte
CChar = _ct.CChar
CCharPtr = _ct.CCharPtr
CVoidPtr = _ct.CVoidPtr
CBool = _ct.CBool
CWchar = _ct.CWchar
CWcharPtr = _ct.CWcharPtr


class _win32:

    # types from Windows.h :
    BYTE = _ct.win32.BYTE
    WORD = _ct.win32.WORD
    DWORD = _ct.win32.DWORD
    CHAR = _ct.win32.CHAR
    WCHAR = _ct.win32.WCHAR
    INT = _ct.win32.INT
    UINT = _ct.win32.UINT
    DOUBLE = _ct.win32.DOUBLE
    FLOAT = _ct.win32.FLOAT
    BOOLEAN = _ct.win32.BOOLEAN
    BOOL = _ct.win32.BOOL
    VARIANT_BOOL = _ct.win32.VARIANT_BOOL
    LONG = _ct.win32.LONG
    ULONG = _ct.win32.ULONG
    SHORT = _ct.win32.SHORT
    USHORT = _ct.win32.USHORT
    WPARAM = _ct.win32.WPARAM
    LPARAM = _ct.win32.LPARAM
    ATOM = _ct.win32.ATOM
    LANGID = _ct.win32.LANGID
    COLORREF = _ct.win32.COLORREF
    LGRPID = _ct.win32.LGRPID
    LCTYPE = _ct.win32.LCTYPE
    LCID = _ct.win32.LCID
    HANDLE = _ct.win32.HANDLE
    HACCEL = _ct.win32.HACCEL
    HBITMAP = _ct.win32.HBITMAP
    HBRUSH = _ct.win32.HBRUSH
    HCOLORSPACE = _ct.win32.HCOLORSPACE
    HDESK = _ct.win32.HDESK
    HDC = _ct.win32.HDC
    HDWP = _ct.win32.HDWP
    HENHMETAFILE = _ct.win32.HENHMETAFILE
    HFONT = _ct.win32.HFONT
    HGDIOBJ = _ct.win32.HGDIOBJ
    HGLOBAL = _ct.win32.HGLOBAL
    HHOOK = _ct.win32.HHOOK
    HICON = _ct.win32.HICON
    HINSTANCE = _ct.win32.HINSTANCE
    HKEY = _ct.win32.HKEY
    HKL = _ct.win32.HKL
    HLOCAL = _ct.win32.HLOCAL
    HMENU = _ct.win32.HMENU
    HMETAFILE = _ct.win32.HMETAFILE
    HMODULE = _ct.win32.HMODULE
    HMONITOR = _ct.win32.HMONITOR
    HPALETTE = _ct.win32.HPALETTE
    HPEN = _ct.win32.HPEN
    HRGN = _ct.win32.HRGN
    HRSRC = _ct.win32.HRSRC
    HSTR = _ct.win32.HSTR
    HTASK = _ct.win32.HTASK
    HWINSTA = _ct.win32.HWINSTA
    HWND = _ct.win32.HWND
    SC_HANDLE = _ct.win32.SC_HANDLE
    SERVICE_STATUS_HANDLE = _ct.win32.SERVICE_STATUS_HANDLE

    # structs from Windows.h :

    RECT = _ct.win32.RECT
    RECTL = _ct.win32.RECTL
    SMALL_RECT = _ct.win32.SMALL_RECT
    _COORD = _ct.win32._COORD
    POINT = _ct.win32.POINT
    POINTL = _ct.win32.POINTL
    SIZE = _ct.win32.SIZE
    SIZEL = _ct.win32.SIZEL
    FILETIME = _ct.win32.FILETIME
    MSG = _ct.win32.MSG
    WIN32_FIND_DATAA = _ct.win32.WIN32_FIND_DATAA
    WIN32_FIND_DATAW = _ct.win32.WIN32_FIND_DATAW


win32: _win32 = _win32()

