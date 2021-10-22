from ctypes import c_bool, c_char_p, c_double, c_long, c_void_p, c_float, c_int, py_object
from _ctypes import CFuncPtr


ERROR_PREFIX = "$*1:"


class CallResults:
    SUCCESS = 0
    FAILURE = 1

    @staticmethod
    def D_FAILURE(error_name: str, error_text: str):
        return f"$*1:{error_name}:{error_text}"

    @staticmethod
    def FAILURE_INFO(failure: str):
        if not failure.startswith(ERROR_PREFIX):
            raise TypeError("Not a detailed failure.")
        data_str = failure.removeprefix(ERROR_PREFIX)
        data = data_str.split(":")
        if data[0] in globals():
            return data[0], data[1]
        raise AttributeError(f"'builtins' object has no attribute '{data[0]}'")


class Dll:
    @staticmethod
    def basic_type_wrap(value):
        if isinstance(value, bool):
            value = c_bool(value)
        elif isinstance(value, float):
            value = c_double(value)
        elif isinstance(value, int):
            value = c_long(value)
        elif isinstance(value, str):
            value = bytes(value, encoding="utf-8")

        else:
            value = py_object(value)
        return value

    @staticmethod
    def basic_type_unwrap(value):
        if isinstance(value, c_char_p):
            value = str(value.value)
        elif isinstance(value, c_bool):
            value = bool(value.value)
        elif isinstance(value, (c_double, c_float)):
            value = float(value.value)
        elif isinstance(value, (c_long, c_int)):
            value = int(value.value)
        elif isinstance(value, (str, bool, float, int, CFuncPtr)):
            pass
        elif isinstance(value, c_void_p):
            if isinstance(value.value, CFuncPtr):
                pass
            else:
                raise ValueError("Return value of function is a C pointer that cannot be converted to PyObject*.")
        else:
            raise ValueError("Return value of function is a C value that cannot be converted to PyObject*.")
        if isinstance(value, str):
            if value.startswith(ERROR_PREFIX):
                error_name, error_text = CallResults.FAILURE_INFO(value)
                raise globals()[error_name](error_text)

        return value

    @staticmethod
    def wrap_self(value):
        return py_object(value)


def format_id(o: object):
    return "0x" + str(hex(id(o))).removeprefix("0x").upper()



