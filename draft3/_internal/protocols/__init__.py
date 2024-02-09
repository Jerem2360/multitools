from typing import Generic

from ._def import Protocol, runtime_checkable
import types


# noinspection PyPropertyDefinition
@runtime_checkable
class WrapsExcInfo(Protocol):
    def __getitem__(self, item: int): ...
    @property
    def type(self) -> type[BaseException] | None: ...
    @property
    def value(self) -> BaseException | None: ...
    @property
    def traceback(self) -> types.TracebackType | None: ...


@runtime_checkable
class IteratesOverCallStack(Protocol):
    def __next__(self) -> types.FrameType: ...


@runtime_checkable
class WrapsCallStack(Protocol):
    def __getitem__(self, item: int) -> types.FrameType | None: ...
    def __len__(self) -> int: ...
    def __iter__(self) -> IteratesOverCallStack: ...


@runtime_checkable
class SupportsBuffer(Protocol):
    def __buffer__(self, flags: int) -> memoryview: ...
    def __buffer_release__(self, buf: memoryview) -> None: ...


@runtime_checkable
class SupportsIndex(Protocol):
    def __index__(self) -> int: ...


@runtime_checkable
class Subscriptable[T](Protocol[T]):
    def __getitem__(self, item) -> T: ...


@runtime_checkable
class SupportsBytes(Protocol):
    def __bytes__(self) -> bytes: ...


@runtime_checkable
class ContextManager(Protocol):
    """
    Represents any object supporting the
    with ... as ... construct
    """
    def __enter__(self): ...
    def __exit__(self, exc_type, exc_val, exc_tb): ...

