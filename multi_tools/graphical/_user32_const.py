from ctypes import c_ulong, wintypes
import _ctypes
import ctypes

DWORD = wintypes.DWORD
HWND = wintypes.HWND
HINSTANCE = wintypes.HINSTANCE
HMENU = wintypes.HMENU
LPVOID = wintypes.LPVOID

_SimpleCData = _ctypes._SimpleCData


def _build_dword_const(value: int) -> DWORD:
    return DWORD(value)


def _build_ulong_const(v: int) -> c_ulong:
    c_l = c_ulong(v)
    return c_l


def consts(a: _SimpleCData, *args: _SimpleCData) -> DWORD:
    for arg in args:
        a.value += arg.value
    return a


PATH = "C:\\Windows\\System32\\user32.dll"


WS_BORDER = _build_dword_const(0x00800000)
WS_CAPTION = _build_dword_const(0x00C00000)
WS_CHILD = _build_dword_const(0x40000000)
WS_CLIPCHILDREN = _build_dword_const(0x02000000)
WS_CLIPSIBLINGS = _build_dword_const(0x04000000)
WS_DISABLED = _build_dword_const(0x08000000)
WS_DLGFRAME = _build_dword_const(0x00400000)
WS_GROUP = _build_dword_const(0x00020000)
WS_HSCROLL = _build_dword_const(0x00100000)
WS_MAXIMIZE = _build_dword_const(0x01000000)
WS_MAXIMIZEBOX = _build_dword_const(0x00010000)
WS_MINIMIZE = _build_dword_const(0x20000000)
WS_MINIMIZEBOX = _build_dword_const(0x00020000)
WS_POPUP = _build_dword_const(0x80000000)
WS_SYSMENU = _build_dword_const(0x00080000)
WS_POPUPWINDOW = consts(WS_POPUP, WS_BORDER, WS_SYSMENU)
WS_TABSTOP = _build_dword_const(0x00010000)
WS_SIZEBOX = _build_dword_const(0x00040000)
WS_TILED = _build_dword_const(0x00000000)
WS_TILEDWINDOW = consts(WS_TILED, WS_CAPTION, WS_SYSMENU, WS_SIZEBOX, WS_MAXIMIZEBOX, WS_MINIMIZEBOX)
WS_VISIBLE = _build_dword_const(0x10000000)
WS_SCROLL = _build_dword_const(0x00200000)
WS_DEFAULT = _build_dword_const(0x00000000)

