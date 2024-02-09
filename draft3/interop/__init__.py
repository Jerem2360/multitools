from .._internal.lang_metadata import NativeLanguage, NativeLanguageStandard, PreprocessorError


def _get_time(context):
    return context.time


def _get_date(context):
    return context.date


def _get_line(context):
    return context.lineno


def _get_file(context):
    return context.filename


def _get_counter(context):
    res = context._counter
    context._counter += 1
    return res


def _defined(context, name):
    return context.defined(name)

