import winreg
import sys

if sys.platform != 'win32':
    raise NotImplementedError("Module is only implemented on Windows.")


class Key:

    def __init__(self, key: winreg.HKEYType, subkey: str):
        self._owner = key
        self._name = subkey
        winreg.CreateKey(key, subkey).Close()

    def set(self, value: str):
        winreg.SetValue(self._owner, self._name, winreg.REG_SZ, value)

    def remove(self):
        winreg.DeleteKey(self._owner, self._name)


class Registry:

    HKEY_CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT
    HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
    HKEY_LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE
    HKEY_USERS = winreg.HKEY_USERS
    HKEY_CURRENT_CONFIG = winreg.HKEY_CURRENT_CONFIG
    HKEY_DYN_DATA = winreg.HKEY_DYN_DATA
    HKEY_PERFORMANCE_DATA = winreg.HKEY_PERFORMANCE_DATA

