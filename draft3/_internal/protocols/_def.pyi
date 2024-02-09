import typing


Interface = Protocol = typing.Protocol
"""
Protocols behave much like interfaces in java or c#.
They define a set of methods and properties that one who
implements them must also define.
To check if an object implements a protocol, use the
isinstance function.
To check if a class implements a protocol, use the 
issubclass function.

There is no need to inherit from an interface to
implement it. The isinstance and issubclass functions
only check the method definitions and their signatures.

Note:

This class isn't actually the typing.Protocol class.
It is exposed as so to make type checkers understand
that it is a Protocol class and not throw errors where
not needed.
"""

runtime_checkable = typing.runtime_checkable
"""
This decorator only exists so type checkers don't complain
about isinstance and issubclass being used with protocols.
This actually isn't the typing.runtime_checkable decorator
and doesn't actually do anything.
"""
