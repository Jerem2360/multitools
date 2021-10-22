from ._user32_impl import *


def CreateWindow(classname: str, h_menu: HMENU, h_instance: HINSTANCE, win_name: str, style: DWORD = WS_DEFAULT, x=0, y=0, width=0,
                 height=0, parent=None, lp_param=None):
    return CreateWindowExA(style, classname, win_name, style, x, y, width, height, parent, h_menu, h_instance,
                           lp_param)



