import winreg
import sys
from typing import Literal, Union
from multi_tools.system.runtime import needsAdmin


if sys.platform != 'win32':
    raise NotImplementedError("Module is only implemented on Windows.")

_RootKeysOnly = Literal[18446744071562067968, 18446744071562067973,  # Accept only Root key values.
                        18446744071562067969, 18446744071562067974,
                        18446744071562067970, 18446744071562067972,
                        18446744071562067971]


_AccesLevel = Literal[983103, 32, 4, 8, 131097, 16, 1, 2, 512, 256, 131078]


class RootHKEYType:
    def __init__(self, key: _RootKeysOnly):
        """
        A type that represents the 7 root registry keys.
        """
        self._value = key
        self._names = {
            winreg.HKEY_CLASSES_ROOT: "HKEY_CLASSES_ROOT",
            winreg.HKEY_USERS: "HKEY_USERS",
            winreg.HKEY_CURRENT_USER: "HKEY_CURRENT_USER",
            winreg.HKEY_LOCAL_MACHINE: "HKEY_LOCAL_MACHINE",
            winreg.HKEY_CURRENT_CONFIG: "HKEY_CURRENT_CONFIG",
            winreg.HKEY_DYN_DATA: "HKEY_DYN_DATA",
            winreg.HKEY_PERFORMANCE_DATA: "HKEY_PERFORMANCE_DATA"
        }

    def get(self):
        """
        Get the integer associated with the registry key.
        """
        return self._value

    @property
    def name(self):
        """
        Get a string representing the name of the key.
        """
        return self._names[self._value]


class Key:

    @needsAdmin
    def __init__(self, key: Union[winreg.HKEYType, RootHKEYType], subkey: str):
        if isinstance(key, RootHKEYType):
            self._owner = key.get()
        elif isinstance(key, winreg.HKEYType):
            self._owner = key
        else:
            raise TypeError("'key' should be an already open key, or any one of the predefined HKEY_* constants.")
        self._owner = key
        self._name = subkey
        self._hkey = winreg.OpenKey(self._owner, self._name)
        self._admin_level = 0
        winreg.CreateKey(key, subkey).Close()

    def edit_rights(self, level: int):
        self._hkey.Close()
        self._hkey = winreg.OpenKey(self._owner, self._name, access=level)

    def get(self):
        return self._hkey

    def set_value(self, value: str):
        winreg.SetValue(self._owner, self._name, winreg.REG_SZ, value)

    def remove(self):
        winreg.DeleteKey(self._owner, self._name)

    @property
    def name(self): return self._name


class GetKey:

    def __init__(self, rootkey: RootHKEYType, *keynames):
        if len(keynames) == 0:
            raise ValueError("At least one key name needs to be provided.")
        else:
            self._name = keynames[-1]

        self._open_keys = []

        new = rootkey.get()
        old = rootkey.get()
        self._owner = rootkey.get()
        for name in keynames:
            new = winreg.OpenKey(old, name)
            self._open_keys.append(new)
            self._owner = old
            old = new

        self._hkey = new

    def get(self):
        return self._hkey

    def set_value(self, value: str):
        winreg.SetValue(self._owner, self._name, winreg.REG_SZ, value)

    def remove(self):
        winreg.DeleteKey(self._owner, self._name)

    def close(self):
        for key in self._open_keys:
            key.Close()

    def edit_rights(self, level: int):
        self._hkey.Close()
        self._hkey = winreg.OpenKey(self._owner, self._name, access=level)

    def __del__(self):
        self.close()


class Registry:
    HKEY_CLASSES_ROOT = RootHKEYType(18446744071562067968)

    HKEY_CURRENT_USER = RootHKEYType(18446744071562067969)

    HKEY_LOCAL_MACHINE = RootHKEYType(18446744071562067970)

    HKEY_USERS = RootHKEYType(18446744071562067971)

    HKEY_CURRENT_CONFIG = RootHKEYType(18446744071562067973)

    HKEY_DYN_DATA = RootHKEYType(18446744071562067974)

    HKEY_PERFORMANCE_DATA = RootHKEYType(18446744071562067972)


class RegistryKeyAccess:
    KEY_ALL_ACCESS = 983103

    KEY_CREATE_LINK = 32

    KEY_CREATE_SUB_KEY = 4

    KEY_ENUMERATE_SUB_KEYS = 8

    KEY_EXECUTE = 131097
    KEY_NOTIFY = 16

    KEY_QUERY_VALUE = 1

    KEY_READ = 131097

    KEY_SET_VALUE = 2

    KEY_WOW64_32KEY = 512
    KEY_WOW64_64KEY = 256

    KEY_WRITE = 131078

