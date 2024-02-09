import inspect
from typing import Self, Iterable

from .protocols import *

class Memory:
    def __init__(self, source: SupportsBuffer | SupportsBytes, readonly: bool = False):
        """
        Create a new Memory object that can access the same memory
        as source. Read and write permissions are preserved.
        """
        # noinspection PyUnresolvedReferences
        self._view = source.__buffer__(inspect.BufferFlags.SIMPLE)

    # noinspection PyUnresolvedReferences
    def __buffer__(self, flags):
        """
        Implement the buffer protocol.
        This allows to do memoryview(self)
        """
        return self._view.__buffer__(flags)

    # noinspection PyUnresolvedReferences
    def __release_buffer__(self, buf):
        """
        Implement the buffer protocol.
        This releases the acquired buffer.
        """
        return self._view.__release_buffer__(buf)

    def __getitem__(self, item: SupportsIndex | slice) -> 'Memory | SupportsIndex':
        """
        Retrieve a segment of the wrapped memory, returned as
        a new Memory object, or the value of a single byte in
        the buffer as an integer.
        The result's Read and Write permissions are inherited from
        the current Memory object.
        """
        if isinstance(item, slice):
            # noinspection PyTypeChecker
            return Memory(self._view[item])
        return self._view[item.__index__()]

    def __setitem__(self, key: SupportsIndex | slice, value: Subscriptable[SupportsIndex] | SupportsIndex):
        """
        Write bytes in the specified segment of the memory buffer.
        The bytes to write can be specified as any kind of buffer or
        list of integers that is at least as long as the segment in which
        it should be written.
        Raises PermissionError for readonly memory.
        """
        if self._view.readonly:
            raise PermissionError("Readonly memory.")
        if isinstance(key, slice):
            start = 0 if key.start is None else key.start
            stop = len(self._view) if key.stop is None else key.stop
            step = 1 if key.step is None else key.step
            j = 0
            for i in range(start, stop, step):
                self._view[i] = value[j].__index__()
                j += 1
            return
        if isinstance(value, Subscriptable):
            value = value[0]
        self._view[key.__index__()] = value

    def __bytes__(self):
        """
        Implement bytes(self)
        """
        return bytes(self[:])

    def __repr__(self):
        """
        Implement repr(self)
        """
        name = type(self).__qualname__
        return f"<{name} {{{' '.join('0x' + hex(i).removeprefix('0x').zfill(2) for i in self[:])}}}>"

    def __len__(self):
        """
        Implement len(self)
        """
        return len(self._view)

    def __iter__(self):
        """
        Iterate over all bytes present in this memory
        buffer. Bytes are yielded as integers.
        """
        return Memory.__iterator__(self)

    def free(self):
        """
        Free the resources associated with the current memory block.
        This only calls the C free() function if the memory is no
        longer needed.
        The caller loses access the associated memory.
        """
        self._view.release()

    def copy(self, dest: 'Memory | None' = None):
        """
        Copy the contents of the current memory block into
        a new or already allocated memory block.
        The destination buffer must be at least as long
        as the current memory block.
        """
        res = dest
        if dest is None:
            res = Memory.malloc(len(self))
        if len(res) < len(self):
            raise OverflowError("Buffer too small.")
        res[:len(self)] = self[:]
        return res

    @classmethod
    def malloc(cls, size: int, readonly: bool = False) -> Self:
        """
        Allocate a new memory block of the specified size.
        If readonly is True, then the resulting memory block
        is readonly.
        """
        res = cls(bytearray(size), readonly)
        return res

    @property
    def writable(self):
        """
        Whether the current memory block can be read.
        """
        return not self._view.readonly

    class __iterator__:
        def __init__(self, target):
            self.target = target.copy()
            self.index = 0

        def __next__(self):
            if self.index >= len(self.target):
                raise StopIteration
            res = self.target[self.index]
            self.index += 1
            return res

