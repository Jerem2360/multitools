
__all__ = [
    'TYPE_CHECKING',
    'ENCODING',
    'BYTEORDER',

    '__ROOT__',
    '__INTERNAL__',
    '__PLATFORM__',
]


from typing import TYPE_CHECKING

from . import platform, runtime, thread


__ROOT__ = ''
__INTERNAL__ = __name__

__PLATFORM__ = platform._PlatformInformation()
if not __PLATFORM__:
    raise NotImplementedError("Unsupported platform architecture.")

ENCODING = platform.encoding
BYTEORDER = platform.byteorder


thread.begin()  # main thread has started, so trigger the setup code.

import _thread as _th
runtime.TState._main = _th.get_ident()

del platform, runtime, thread, _th

