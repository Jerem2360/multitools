from typing import overload, List, final, Union
from _io import TextIOWrapper
from time import sleep as wait
from multi_tools import data
import os


registry = data.Registry()


class TextIO:

    @overload
    def __init__(self, file: str, customName=None): ...

    @overload
    def __init__(self, io_stream: TextIOWrapper, customName=None): ...

    def __init__(self, x=None, customName=None):
        """
        Create an return a basic IO stream.

        Signatures:

        - TextIO(file: str, __customName: Optional[str])

          Create a IO stream that points to the file 'file'.

        - TextIO(io_stream: _io.TextIOWrapper, __customName: Optional[str])

          Create a IO stream that points to the same file as 'io_stream' and has the same type as it.
        """
        self._name = None
        self._io_stream = None
        if isinstance(x, str):
            self._io_stream = _Stream(x)

        elif isinstance(x, TextIOWrapper):
            self._io_stream = x

        else:
            raise TypeError(f"Expected str or TextIOWrapper, got {type(x)} instead.")

        if customName is None:
            self._name = self._io_stream.name
        else:
            self._name = customName

        registry.save(self._name, self)

    @final
    def write(self, text: str, cut_content=True, end="\n") -> None:
        """
        Write (text + end) to the file the IO stream points to.
        Works only if type is 'IO' or 'O'.
        As the above '@final' suggests, this method isn't
        overrideable.
        """
        original_file = ""
        if not cut_content:
            if self._io_stream.readable():
                original_file = self.__read__(-1)

        to_write = original_file + text + end

        if self._io_stream.writable():
            self.__write__(to_write)
        else:
            wait(0.1)
            raise BlockingIOError(f"Object \"{self._name}\" cannot be written to.")

    @final
    def read(self, size=1) -> str:
        """
        Read from the file the IO stream points to and return the result.
        Works only if type is 'IO' or 'I'.
        As the above '@final' suggests, this method isn't
        overrideable.
        """
        if not self._io_stream.readable():
            wait(0.1)
            raise BlockingIOError(f"Object \"{self._name}\" cannot be read.")

        return self.__read__(size=size)

    @final
    def readlines(self) -> List[str]:
        """
        Pretty much the same as read().
        As the above '@final' suggests, this method isn't
        overrideable.
        """
        return self.read().split("\n")

    @final
    def configure(self, new_target: str or TextIOWrapper):
        """
        Changes the file on which the IO stream points for new_target.
        As the above '@final' suggests, this method isn't
        overrideable.
        """
        self.__redirect__(new_target)

    def __write__(self, text: str):
        """
        Write text to stream. Can be overridden.
        **Doesn't handle any error, you should use write() instead**
        """
        self._io_stream.write(text)

    def __read__(self, size: int, spec=False):
        """
        Read text from stream and return. Can be overridden.
        **Doesn't handle any error, you should use read() instead**
        """
        if spec:  # 'spec' is a specific parameter used only by multi_tools.console.io.IStream. It should not be used anywhere else.
            return input()  # temporary, while looking for a working self._io_stream.readline()

        return self._io_stream.read(size)

    @overload
    def __redirect__(self, file: str, customName: str = None): ...

    @overload
    def __redirect__(self, io_stream: TextIOWrapper, customName: str = None): ...

    def __redirect__(self, x=None, customName=None):  # real signature is __redirect__(self, x: TextIOWrapper or str) -> TextIO
        """
        **Do not use directly**
        """
        # save old values:
        buffer = self

        # set new values for attributes:
        self._name = None
        self._io_stream = None
        if isinstance(x, str):
            self._io_stream = _Stream(x)

        elif isinstance(x, TextIOWrapper):
            self._io_stream = x

        else:
            raise TypeError(f"Expected str or TextIOWrapper, got {type(x)} instead.")

        if customName is None:
            self._name = self._io_stream.name
        else:
            self._name = customName

        return buffer

    def _stream_type(self):
        stream_type = ""
        if self._io_stream.readable():
            stream_type += "I"
        if self._io_stream.writable():
            stream_type += "O"
        return stream_type

    def __repr__(self):

        return f"<TextIO at {id(self)}, name='{self._name}', type={self._stream_type()}>"

    def flush(self): self._io_stream.flush()

    @staticmethod
    def by_name(name: str):
        return registry[name]

    @property
    def type(self): return self._stream_type()


class _Stream:
    def __init__(self, path: str):
        """
        Path string to IO stream with type 'IO' converter.
        **Only for internal use**
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"Unknown file or directory \"{path}\".")
        if not os.path.isfile(path):
            raise FileNotFoundError(f"Object \"{path}\" not a file.")

        if "\\" in path:
            self.name = path.split("\\")[len(path.split("\\")) - 1]
        else:
            self.name = path.split("/")[len(path.split("/")) - 1]

        self._path = path
        self._IO = None

    def write(self, __s: str) -> int:
        open_mode = "w+"
        self._IO = open(self._path, mode=open_mode)
        self._IO.write(__s)
        self._IO.close()
        return len(__s)

    def read(self) -> str:
        open_mode = "r+"

        self._IO = open(self._path, mode=open_mode)
        result = self._IO.read()
        self._IO.close()
        return result

    @classmethod
    def readable(cls): return True

    @classmethod
    def writable(cls): return True

