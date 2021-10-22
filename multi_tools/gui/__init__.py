# from . import tcl
from sys import executable as _exe_path


_py_path = _exe_path.removesuffix(r"\python.exe")
_tcl_path = r"\DLLs\tcl86t.dll"
_tk_path = r"\DLLs\tk86t.dll"


IMPORT_TK = "package require Tk"

TCL_DLL = _py_path + _tcl_path

print(TCL_DLL)

