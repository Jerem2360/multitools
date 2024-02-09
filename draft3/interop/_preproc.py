

def _split_into_tokens(preproc, cond):
    operators = ('==', '&&', '||', '^', '!=', '<', '>', '<=', '>=')
    tokens = ['']

    for char in cond:
        if char == ' ':
            tokens.append('')
            continue

        if char in ('|', '&', '^', '='):
            if (tokens[-1] + char) in operators:
                tokens[-1] += char
                tokens.append('')
                continue

            tokens.append(char)
            continue

        if char == '!':
            tokens.append(char)
            continue

        if char in ('(', ')'):
            tokens.append(char)
            tokens.append('')
            continue

        if char in '<>':
            tokens.append('')
            tokens.append(char)
            continue

        if tokens[-1] in ('!', '|', '&', '^', '=', '<', '>'):
            tokens.append('')

        tokens[-1] += char

    while True:
        try:
            i = tokens.index('')
        except ValueError:
            break
        tokens.pop(i)

    return tokens


def eval_condition(preproc, cond):
    operators = {'==', '&&', '||', '^', '!=', '<', '>', '<=', '>='}
    tokens = _split_into_tokens(preproc, cond)
    memory = [[], []]
    bracketlevel = 0
    operand = 0
    res = True

    i = -1

    while True:
        i += 1
        if i >= len(tokens):
            break

        if tokens[i] == '(':
            bracketlevel += 1
            continue

        if tokens[i] == ')':
            bracketlevel -= 1
            continue

        if tokens[i] in operators:



    return res


def pad_line(line: str):
    ignore = ('\t', '\r', '\x00')

    for char in ignore:
        line = line.replace(char, '')
    line = line.split('//', 1)[0]
    return line.lstrip().rstrip()


def c_line(preproc, line):
    commentless_line = ''
    from .._internal.lang_metadata import PreprocessorError

    # print(preproc._multiline_comment)

    entire_line = True
    if '/*' in line and not preproc._multiline_comment:
        commentless_line += line.split('/*', 1)[0]
        preproc._multiline_comment = True
        entire_line = False

    if '*/' in line:
        if not preproc._multiline_comment:
            raise PreprocessorError(preproc, "Invalid 'END_COMMENT' token.")
        commentless_line += line.rsplit('*/', 1)[-1]
        preproc._multiline_comment = False
        entire_line = False

    if not preproc._multiline_comment and entire_line:
        commentless_line = line

    if not commentless_line:
        return commentless_line

    if commentless_line.startswith('#'):
        directive_name = commentless_line.split(' ', 1)[0].removeprefix('#')
        directive = preproc.standard._directives.get(directive_name, None)
        if directive is None:
            raise PreprocessorError(preproc, f"Unknown preprocessor directive '{directive_name}'.")
        arg = commentless_line.split(' ', 1)[-1]
        line = directive(preproc, arg)
        # print(directive_name, arg, line)
        if not line:
            return ''
        if line == 1:
            return line
    elif not preproc._calculate_ifs():
        return ''

    return line


def c_preprocessor(preproc, code):
    preproc._lineno = 1
    res_lines = []
    input_lines = list(pad_line(ln) for ln in code.split('\n'))

    for line in input_lines:
        res_line = c_line(preproc, line)
        if res_line == 1 and preproc._filename in preproc._parsed:
            return []
        if isinstance(res_line, str) and res_line:
            res_lines.append(res_line)
        preproc._lineno += 1

    return res_lines

