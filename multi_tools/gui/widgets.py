

class Widget:
    __slots__ = ["long_name", "name", "_tcl_interp", "_creating_command", "_show_type", "_widname"]

    def __init__(self, _tcl_interp, parent, name):
        self._creating_command = None
        self._show_type = None
        self._widname = None

        self._tcl_interp = _tcl_interp
        self.name = name
        if isinstance(parent, Widget):
            self.long_name = f"{parent.long_name}.{self.name}"
        else:
            self.long_name = self.name

    def wm_create(self, opt1, opt2):
        # self._create_command = f"{self._show_type} [ttk::{self._widname} .{self.long_name}]"
        wid_data = self._tcl_interp.build_command("ttk::" + self._widname, "." + self.long_name, *opt1)
        self._creating_command = self._tcl_interp.build_command(self._show_type, f"[{wid_data}]", *opt2)

    def __create__(self, *args, **kwargs):
        self.wm_create({}, {})

