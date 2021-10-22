from ._user32_const import *
from ..system import DllImport
from ctypes import c_void_p as _VoidPtr, Structure as _Struct


@DllImport(PATH)
def CreateWindowExA(dwExStyle: DWORD, lpClassName: str, lpWindowName: str, dwStyle: DWORD, X: int, Y: int,
                    nWidth: int, nHeight: int, hWndParent: HWND, hMenu: HMENU, hInstance: HINSTANCE,
                    lpParam: LPVOID) -> HWND:
    """
    Create and return a new HWND window handle.
    Return None upon failure.
    """

