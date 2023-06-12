"""
Library offering various system-related tools.

It does several things when imported.
Let me call the 'importer scope' the current scope at the moment where
multitools was imported by a program.

Inside the importer scope and all of its subsequent scopes (except C function calls),
the behaviour of the 'raise' statement is modified as follows:
If an ExceptionInformation instance is passed in the 'from' clause of the 'raise'
statement, it is stored inside the exception object as the '__info__' attribute.
Proceeding this way modifies how the exception is raised and printed to the console.
See the docs of the ExceptionInformation class for details.
"""


__all__ = [
    '__author__',
    '__version__',
    '_called',
]


__version__ = '2.0'
__author__ = 'Jerem2360'

from . import _internal


_internal.__ROOT__ = __name__
del _internal
_called = False

