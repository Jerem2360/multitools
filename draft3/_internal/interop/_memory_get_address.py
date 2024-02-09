import ctypes
from .. import memory


class _Py_buffer(ctypes.Structure):  # the Py_Buffer structure from the C api
    _fields_ = (
        ("_buf", ctypes.c_void_p),
        ("_obj", ctypes.c_void_p),
        ("_len", ctypes.c_ssize_t),
        ("_itemsize", ctypes.c_ssize_t),
        ("_readonly", ctypes.c_int),
        ("_ndim", ctypes.c_int),
        ("_format", ctypes.c_char_p),
        ("_shape", ctypes.c_void_p),
        ("_strides", ctypes.c_void_p),
        ("_suboffsets", ctypes.c_void_p),
        ("_internal", ctypes.c_void_p),
    )

    @property
    def target_address(self):
        return ctypes.c_void_p(self._buf)

ctypes.pythonapi.PyObject_GetBuffer.argtypes = (ctypes.py_object, ctypes.POINTER(_Py_buffer), ctypes.c_int)
ctypes.pythonapi.PyObject_GetBuffer.restype = ctypes.c_int

def mem_addressof(mem: memory.Memory):
    buf = _Py_buffer()

    if ctypes.pythonapi.PyObject_GetBuffer(ctypes.py_object(mem), ctypes.byref(buf), ctypes.c_int(0)) < 0:
        return 0

    return buf.target_address

