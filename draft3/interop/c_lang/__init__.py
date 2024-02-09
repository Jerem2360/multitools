from .. import NativeLanguage, NativeLanguageStandard, _get_date, _get_time, _get_file, _get_line, _get_counter


__language__ = NativeLanguage("C")

__stdc89__ = NativeLanguageStandard(__language__, "C89", 198901,
                                    __STDC__=1,
                                    __STDC_VERSION__=198901,
                                    __STDC_HOSTED__=0,
                                    __DATE__=_get_date,
                                    __TIME__=_get_time,
                                    __FILE__=_get_file,
                                    __LINE__=_get_line,
                                    __COUNTER__=_get_counter,
                                    )
__language__._register_std(__stdc89__)

__stdc90__ = NativeLanguageStandard(__language__, "C90", 199001,
                                    __STDC__=1,
                                    __STDC_VERSION__=199001,
                                    __STDC_HOSTED__=0,
                                    __DATE__=_get_date,
                                    __TIME__=_get_time,
                                    __FILE__=_get_file,
                                    __LINE__=_get_line,
                                    __COUNTER__=_get_counter,
                                    )
__language__._register_std(__stdc90__)

__stdc95__ = NativeLanguageStandard(__language__, "C95", 199409,
                                    __STDC__=1,
                                    __STDC_VERSION__=199409,
                                    __STDC_HOSTED__=0,
                                    __DATE__=_get_date,
                                    __TIME__=_get_time,
                                    __FILE__=_get_file,
                                    __LINE__=_get_line,
                                    __COUNTER__=_get_counter,
                                    )
__language__._register_std(__stdc95__)

__stdc99__ = NativeLanguageStandard(__language__, "C99", 199901,
                                    __STDC__=1,
                                    __STDC_VERSION__=199901,
                                    __STDC_HOSTED__=0,
                                    __DATE__=_get_date,
                                    __TIME__=_get_time,
                                    __FILE__=_get_file,
                                    __LINE__=_get_line,
                                    __STDC_IEC_559__=1,
                                    __STDC_IEC_559_COMPLEX__=1,
                                    __COUNTER__=_get_counter,
                                    )
__language__._register_std(__stdc99__)

__stdc11__ = NativeLanguageStandard(__language__, "C11", 201112,
                                    __STDC__=1,
                                    __STDC_VERSION__=201112,
                                    __STDC_HOSTED__=0,
                                    __STDC_NO_ATOMICS__=0,
                                    __STDC_NO_COMPLEX__=0,
                                    __STDC_NO_THREADS__=0,
                                    __STDC_NO_VLA__=0,
                                    __DATE__=_get_date,
                                    __TIME__=_get_time,
                                    __FILE__=_get_file,
                                    __LINE__=_get_line,
                                    __STDC_IEC_559__=1,
                                    __STDC_IEC_559_COMPLEX__=1,
                                    __STDC_ANALYZABLE__=1,
                                    __STDC_LIB_EXT1__=1,
                                    __COUNTER__=_get_counter,
                                    )
__language__._register_std(__stdc11__)

__stdc17__ = NativeLanguageStandard(__language__, "C17", 201710,
                                    __STDC__=1,
                                    __STDC_VERSION__=201710,
                                    __STDC_HOSTED__=0,
                                    __STDC_NO_ATOMICS__=0,
                                    __STDC_NO_COMPLEX__=0,
                                    __STDC_NO_THREADS__=0,
                                    __STDC_NO_VLA__=0,
                                    __DATE__=_get_date,
                                    __TIME__=_get_time,
                                    __FILE__=_get_file,
                                    __LINE__=_get_line,
                                    __STDC_IEC_559__=1,
                                    __STDC_IEC_559_COMPLEX__=1,
                                    __STDC_ANALYZABLE__=1,
                                    __STDC_LIB_EXT1__=1,
                                    __COUNTER__=_get_counter,
                                    )
__language__._register_std(__stdc17__)

__stdc23__ = NativeLanguageStandard(__language__, "C23", 202301,
                                    __STDC__=1,
                                    __STDC_VERSION__=202301,
                                    __STDC_HOSTED__=0,
                                    __STDC_NO_ATOMICS__=0,
                                    __STDC_NO_COMPLEX__=0,
                                    __STDC_NO_THREADS__=0,
                                    __STDC_NO_VLA__=0,
                                    __DATE__=_get_date,
                                    __TIME__=_get_time,
                                    __FILE__=_get_file,
                                    __LINE__=_get_line,
                                    __STDC_IEC_559__=1,
                                    __STDC_IEC_559_COMPLEX__=1,
                                    __STDC_ANALYZABLE__=1,
                                    __STDC_LIB_EXT1__=1,
                                    __COUNTER__=_get_counter,
                                    )
__language__._register_std(__stdc23__)

@__language__.preprocessor_implementation
def __parse__(preproc, contents):
    from .._preproc import c_preprocessor as base
    lines = base(preproc, contents)
    return '\n'.join(lines)


@__stdc89__._directive('if')
@__stdc90__._directive('if')
@__stdc95__._directive('if')
@__stdc99__._directive('if')
@__stdc11__._directive('if')
@__stdc17__._directive('if')
@__stdc23__._directive('if')
def IfDirective(preproc, arg):
    from .._preproc import eval_condition as base
    preproc._push_if(base(preproc, arg))
    return True


@__stdc89__._directive('else')
@__stdc90__._directive('else')
@__stdc95__._directive('else')
@__stdc99__._directive('else')
@__stdc11__._directive('else')
@__stdc17__._directive('else')
@__stdc23__._directive('else')
def ElseDirective(preproc, arg):
    preproc._invert_if()


@__stdc89__._directive('elif')
@__stdc90__._directive('elif')
@__stdc95__._directive('elif')
@__stdc99__._directive('elif')
@__stdc11__._directive('elif')
@__stdc17__._directive('elif')
@__stdc23__._directive('elif')
def ElifDirective(preproc, arg):
    from .._preproc import eval_condition as base
    preproc._pop_if()
    preproc._push_if(base(preproc, arg))


@__stdc89__._directive('endif')
@__stdc90__._directive('endif')
@__stdc95__._directive('endif')
@__stdc99__._directive('endif')
@__stdc11__._directive('endif')
@__stdc17__._directive('endif')
@__stdc23__._directive('endif')
def EndifDirective(preproc, arg):
    preproc._pop_if()


@__stdc89__._directive('ifdef')
@__stdc90__._directive('ifdef')
@__stdc95__._directive('ifdef')
@__stdc99__._directive('ifdef')
@__stdc11__._directive('ifdef')
@__stdc17__._directive('ifdef')
@__stdc23__._directive('ifdef')
def IfDefDirective(preproc, arg):
    trueness = preproc.defined(arg)
    preproc._push_if(trueness)


@__stdc23__._directive('elifdef')
def ElifDefDirective(preproc, arg):
    trueness = preproc.defined(arg)
    preproc._pop_if()
    preproc._push_if(trueness)


@__stdc89__._directive('error')
@__stdc90__._directive('error')
@__stdc95__._directive('error')
@__stdc99__._directive('error')
@__stdc11__._directive('error')
@__stdc17__._directive('error')
@__stdc23__._directive('error')
def ErrorDirective(preproc, arg):
    from .. import PreprocessorError
    if not preproc._calculate_ifs():
        return
    raise PreprocessorError(preproc, eval(arg))


@__stdc89__._directive('include')
@__stdc90__._directive('include')
@__stdc95__._directive('include')
@__stdc99__._directive('include')
@__stdc11__._directive('include')
@__stdc17__._directive('include')
@__stdc23__._directive('include')
def IncludeDirective(preproc, arg):
    from .. import PreprocessorError
    import os
    if not preproc._calculate_ifs():
        return
    if arg.startswith('"') and arg.endswith('"'):
        filename = arg.removeprefix('"').removesuffix('"')
        current_file_path = preproc.filename.rsplit(os.path.sep, 1)[0] if os.path.sep in preproc.filename else os.getcwd()
        cache = os.getcwd()
        os.chdir(current_file_path)
        if not os.path.exists(filename):
            raise PreprocessorError(preproc, f"Unknown file '{filename}'.")
        res = preproc.parse(filename)
        os.chdir(cache)
        return res

    if arg.startswith('<') and arg.endswith('>'):
        filename = arg.removeprefix('<').removesuffix('>')
        cache = os.getcwd()
        os.chdir(preproc.libc)
        if not os.path.exists(filename):
            raise PreprocessorError(preproc, f"Unknown file <{filename}>.")

        res = preproc.parse(filename)
        os.chdir(cache)
        return res


@__stdc89__._directive('pragma')
@__stdc90__._directive('pragma')
@__stdc95__._directive('pragma')
@__stdc99__._directive('pragma')
@__stdc11__._directive('pragma')
@__stdc17__._directive('pragma')
@__stdc23__._directive('pragma')
def PragmaDirective(preproc, arg):
    from .. import PreprocessorError
    if not preproc._calculate_ifs():
        return
    # print(preproc.filename, preproc._parsed, preproc.filename in preproc._parsed, arg)
    if (arg == 'once') and (preproc.filename in preproc._parsed):
        return 1

    if arg.startswith('pack('):
        temp = arg.removeprefix('pack(')
        if not temp.endswith(')'):
            raise PreprocessorError(preproc, "#pragma pack: invalid syntax.")
        _arg: str = temp.removesuffix(')')
        args = _arg.split(', ')
        if len(args) == 0:
            raise PreprocessorError(preproc, "#pragma pack: 1 or 2 arguments expected.")
        op_s = args[0]

        match op_s:
            case 'push':  # pragma pack(push, val)
                if len(args) != 2:
                    raise PreprocessorError(preproc, "#pragma pack: push requires a second argument to pack.")
                val_s = args[1]
                if not val_s.isdigit():
                    raise PreprocessorError(preproc, "#pragma pack: second argument must be an integer.")
                val = int(val_s)
                preproc._pack.append(val)

            case 'pop':  # pragma pack(pop)
                if len(preproc._pack):
                    preproc._pack.pop(-1)

        return


@__stdc89__._directive('define')
@__stdc90__._directive('define')
@__stdc95__._directive('define')
@__stdc99__._directive('define')
@__stdc11__._directive('define')
@__stdc17__._directive('define')
@__stdc23__._directive('define')
def DefineDirective(preproc, arg):
    from .. import PreprocessorError
    info = ['', '', '']  # name, params, def

    bracketlevel = 0
    status = 0

    for char in arg:
        if char == '(':
            bracketlevel += 1
        if char == ')':
            bracketlevel -= 1
            if bracketlevel < 0:
                raise PreprocessorError(preproc, "Too many ')' tokens.")

        if status == 0 and char == '(':
            status += 1

        if status in (0, 1) and bracketlevel == 0 and char == ' ':
            status = 2
            continue

        info[status] += char

    name = info[0]
    params = list(a.strip() for a in info[1].removeprefix('(').removesuffix(')').split(','))
    definition = info[2]

    while True:
        try:
            i = params.index('')
        except ValueError:
            break

        params.pop(i)

    params = tuple(params)

    preproc.define(name, definition, params)


@__stdc89__._directive('undef')
@__stdc90__._directive('undef')
@__stdc95__._directive('undef')
@__stdc99__._directive('undef')
@__stdc11__._directive('undef')
@__stdc17__._directive('undef')
@__stdc23__._directive('undef')
def UndefDirective(preproc, arg):
    preproc.undef(arg)

