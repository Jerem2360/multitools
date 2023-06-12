"""
Private platform api.
"""


import sys


class _PlatformInformation:
    __slots__ = (
        'system',
        'win32',
        'linux',
        'mac',
        'jython',
        'type',
        'id',
        'linkage',
        'is32bit',
        'is64bit',
        'version',
    )

    def __init__(self):
        import sys
        import os
        import platform

        self.system = platform.system()
        self.win32 = False
        self.linux = False
        self.mac = False
        self.jython = False
        if self.system == '':
            return

        self.type = os.name
        self.id = sys.platform
        b, self.linkage = platform.architecture()

        match self.system:
            case 'Windows':
                self.version = platform.win32_ver()
                self.is64bit = b == '64bit'
                self.is32bit = b == '32bit'
                self.win32 = True

            case 'Linux':
                self.version = platform.libc_ver()
                self.is64bit = b == '64bit'
                self.is32bit = b == '32bit'
                self.linux = True

            case 'Darwin':
                self.version = platform.mac_ver()
                self.is64bit = sys.maxsize > 2**32
                self.is32bit = sys.maxsize <= 2**32
                self.mac = True

            case 'Java':
                self.version = platform.java_ver()
                self.is64bit = b == '64bit'
                self.is32bit = b == '32bit'
                self.jython = True

    def __bool__(self):
        return self.system != ''

    def __dir__(self):
        return type(self).__slots__


byteorder = sys.byteorder
encoding = sys.getdefaultencoding()

