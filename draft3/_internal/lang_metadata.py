import os.path
from typing import Callable


class NativeLanguage:
    def __init__(self, name):
        self._name = name
        self._stds = {}
        self._preproc_implementation = lambda preproc, _input: _input

    def _register_std(self, std):
        self._stds[std.name] = std

    def get_standard(self, name: str) -> 'NativeLanguageStandard':
        return self._stds.get(name, None)

    def create_preprocessor(self, standard: str):
        return Preprocessor(self, standard)

    def preprocessor_implementation(self, func: Callable[['Preprocessor', str], str]):
        self._preproc_implementation = func
        return func

    @property
    def name(self) -> str:
        return self._name



class NativeLanguageStandard:
    def __init__(self, language: NativeLanguage, std_name: str, std_id: int, **default_macros):
        self._lang = language
        self._name = std_name
        self._default_macros = default_macros
        self._id = std_id
        self._directives = {}

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def default_macros(self) -> dict[str, ...]:
        return self._default_macros

    @property
    def language(self) -> NativeLanguage:
        return self._lang

    def _register_directive(self, name, func):
        self._directives[name] = func

    def _directive(self, name):
        def _inner(func):
            self._directives[name] = func
            return func

        return _inner


class Macro:
    def __init__(self, name: str, value):
        self._name = name
        self._value = value

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    def expand(self, *args):
        return self._value


class ParametrizedMacro(Macro):
    def __init__(self, name: str, value: str, *parameters: str):
        super().__init__(name, value)
        self._params = parameters

    def expand(self, *args: str):
        res = self.value
        for i in range(len(self._params)):
            try:
                param = self._params[i]
            except:
                raise TypeError("Too much arguments passed to macro.")
            try:
                arg = args[i]
            except:
                res = res.replace(param, "")
                continue
            res = res.replace(param, arg)
        return res


class Preprocessor:
    def __init__(self, language: NativeLanguage, standard: str):
        self._lang = language
        self._std = language.get_standard(standard)
        self._macros = {}
        for k, v in self._std.default_macros.items():
            self._macros[k] = Macro(k, v)
        self._counter = 0
        self._filename = None
        self._lineno = None
        self._time = None
        self._date = None
        self._multiline_comment = False
        self._if_level = 0
        self._if_conditions = [True]
        self._parsed = []
        self._pack = [8]
        self._libc_path = 'C:\\Program Files\\Microsoft Visual Studio\\2022\\Community\\VC\\Tools\\MSVC\\14.37.32822\\include'

    def define(self, name, value=None, params=(), /):
        if len(params):
            self._macros[name] = ParametrizedMacro(name, value, params)
            return
        self._macros[name] = Macro(name, value)

    def undef(self, name, /):
        try:
            del self._macros[name]
        except:
            return False
        return True

    def defined(self, name, /):
        return name in self._macros

    def get_macro(self, name, /):
        res = self._macros.get(name, None)
        if callable(res):
            return res(self)
        return res

    def parse(self, filename):
        _prev_file = self._filename
        import os
        with open(filename) as fs:
            contents = fs.read()

        self._filename = os.path.realpath(filename)
        self._lineno = 1

        res = self.language._preproc_implementation(self, contents)
        self._parsed.append(os.path.realpath(filename))
        self._filename = _prev_file
        return res

    @property
    def filename(self):
        if self._filename is not None:
            return self._filename
        from .. import thread
        ts = thread.TState.current()
        return ts.call_stack[3].f_code.co_filename

    @property
    def lineno(self):
        if self._lineno is not None:
            return self._lineno
        from .. import thread
        ts = thread.TState.current()
        return ts.call_stack[3].f_lineno

    @property
    def language(self):
        return self._lang

    @property
    def standard(self):
        return self._std

    @property
    def date(self):
        if self._date is not None:
            return self._date
        import datetime
        dow, month, day, time, year = datetime.datetime.now(datetime.UTC).ctime().split(' ')
        return " ".join((month, day, year))

    @property
    def time(self):
        if self._time is not None:
            return self._time
        import datetime
        return datetime.datetime.now(datetime.UTC).ctime()

    @property
    def libc(self):
        return self._libc_path

    @libc.setter
    def libc(self, value):
        if not os.path.exists(value):
            raise NotADirectoryError(value)
        self._libc_path = value

    def _push_if(self, trueness):
        self._if_conditions.append(trueness)

    def _invert_if(self):
        self._if_conditions[-1] = not self._if_conditions[-1]

    def _pop_if(self):
        self._if_conditions.pop(-1)

    def _calculate_ifs(self):
        for cond in self._if_conditions:
            if not cond:
                return False
        return True

    def _error(self, op):
        raise PreprocessorError(self, op)


class Directive:
    def __init__(self, name, func):
        self._name = name
        self._proc = func

    def __call__(self, preproc, arg):
        return self._proc(preproc, arg)

class PreprocessorError(Exception):
    def __init__(self, preproc, msg):
        super().__init__(f"File '{preproc.filename}', line {preproc.lineno}: {msg}")

