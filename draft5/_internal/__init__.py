
PATH_SEP = __import__("os").path.sep
"""
Character used to separate nodes in a filesystem path.
This usually is '\\' on windows and '/' elsewhere. 
"""

__root__: str = __name__.rsplit('.', 1)[0]
"""
The name of multitools' root package as reported by sys.modules.
"""

__internal_path__ = __file__.rsplit(PATH_SEP, 1)[0]
"""
The filename that should be used when multitools internal code
is to be located, e.g. for tracebacks.
This refers to a directory and not a file.
"""

__internal_file__ = __internal_path__ + PATH_SEP + '__init__.py'
"""
Version of __internal_path__ that is a valid file on the file system
instead of just a directory. 
"""


from . import interpreter

interpreter.MainInterpreterState()

from . import overwrite

