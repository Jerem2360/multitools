from . import TCL_DLL as TCL_PATH
from multi_tools.cpp import HeaderClass, HeaderFunc
from multi_tools.system.dll import VoidPointer, Array
from multi_tools.system import DllImport


@DllImport(TCL_PATH)
def Tcl_Free(pointer: VoidPointer) -> None:
    """
    Free the memory for 'pointer'.
    """


@HeaderClass(TCL_PATH)
class _Tcl:

    @staticmethod
    @HeaderFunc
    def Tcl_CreateInterp() -> VoidPointer:
        """
        Create a tcl interpreter.
        """

    @staticmethod
    @HeaderFunc
    def Tcl_CreateObjCommand(interpreter: VoidPointer, cmd_name: str, command: str, ClientData, DeleteProc):
        """
        Create tcl command object.
        """
    @staticmethod
    @HeaderFunc
    def Tcl_Init(interpreter: VoidPointer):
        """
        Initialize tcl interpreter.
        """

    @staticmethod
    @HeaderFunc
    def Tcl_ProcObjCmd(interpreter: VoidPointer, args: Array):
        """
        Create new tcl procedure.
        """

    @staticmethod
    @HeaderFunc
    def Tcl_EvalObj(interpreter: VoidPointer, command: VoidPointer):
        """
        Evaluate a tcl command and execute it.
        """

    def __init__(self):
        self._interpreter = self.Tcl_CreateInterp()
        self.Tcl_Init(self._interpreter)

    def _make_command(self, command_args: list[str]):
        c_args = Array(*[_Tcl_Str(v).get() for v in command_args])

        tcl_procedure = self.Tcl_ProcObjCmd(self._interpreter, c_args)
        tcl_command = self.Tcl_CreateObjCommand(self._interpreter, "Py_Command", tcl_procedure)
        return tcl_command

    def _call_command(self, tcl_command: VoidPointer):
        return self.Tcl_EvalObj(self._interpreter, tcl_command)

    def call(self, command_name: str, *args):
        """
        Call command 'command_name' with arguments 'args'.
        Return the command's return value.
        """
        Tcl_command = self._make_command([command_name, *args])
        return self._call_command(Tcl_command)


@HeaderClass(TCL_PATH)
class _Tcl_Str:
    @staticmethod
    @HeaderFunc
    def Tcl_NewStringObj(value: str) -> VoidPointer:
        """
        Create tcl string.
        """

    def __init__(self, value: str):
        self._value: VoidPointer = self.Tcl_NewStringObj(value)

    def get(self):
        return self._value

    def __del__(self):
        Tcl_Free(self._value)


class TkLib:
    __slots__ = ["_tcl_interp"]

    def __init__(self):
        self._tcl_interp = _Tcl()
        self._tcl_interp.call("package", "require", "Tk")

    @staticmethod
    def build_command(arg1: str, *args):
        cmd_args = list(args)
        cmd_args.insert(0, arg1)
        return cmd_args

    def wm_title(self, title: str):
        self._tcl_interp.call("wm", "title", ".", title)

    def wait_forever(self):
        self._tcl_interp.call("vwait", "forever")




