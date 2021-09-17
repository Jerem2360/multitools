from multi_tools.cpp import HeaderClass, HeaderFunc
from multi_tools import config


class Address:
    def __init__(self, address: int):
        """
        An address can be formatted, converted to hex, to int, or to str.
        """
        self._ad = address

    def __repr__(self):
        return hex(self._ad)

    def __int__(self):
        return self._ad

    def __hex__(self):
        return hex(self._ad)

    def __str__(self):
        return str(hex(self._ad))

    def format(self):
        negative = False
        str_address = str(hex(self._ad))
        if str_address.startswith('-'):
            negative = True

        address_no_prefix = str_address.removeprefix('0x').removeprefix('-0x')
        hex_ = '0x' + address_no_prefix.upper()
        if negative:
            hex_ = '-' + hex_

        return hex_


@HeaderClass("pointer.dll", type_=config.Cpp.WinDLL, no_errors=True)
class Pointer:
    """
    A simple pointer type that points to a specific object's location in memory.
    If 'pointer.dll' does not exist, this class is useless.
    """
    @HeaderFunc
    def __init__(self, target) -> None:
        """
        Create and return a new pointer to 'target'.
        """
        pass

    def __repr__(self) -> str:
        return f"<Pointer to '{Address(self._getaddress())}' at {Address(id(self)).format()}>"

    @HeaderFunc
    def _getaddress(self) -> int:
        """
        Get the numerical address self points to.
        """
        pass

    @property
    def address(self):
        """
        The address of self, in form of an Address object.
        """
        return Address(self._getaddress())


def addressof(__object: object) -> Pointer:
    """
    Return a pointer to __object.
    """
    return Pointer(__object)
