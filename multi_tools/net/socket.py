from typing import Union, Any
import socket


class _Sock:
    socket_bufsize = 256
    socket_encoding = "utf-8"

    def __init__(self, __family, __type, proto=-1, fileno=None):
        self._s = socket.socket(__family, __type, proto, fileno=fileno)

    def __write__(self, data: bytes) -> int:
        return self._s.send(data)

    def __read__(self, buffersize: int) -> bytes:
        return self._s.recv(buffersize)

    @classmethod
    def readable(cls): return True

    @classmethod
    def writable(cls): return True

    def write(self, data: Union[str, bytes]) -> int:
        dta = bytes(data)
        return self.__write__(dta)

    def read(self, buffersize=None, ret_type: type = bytes) -> Any:
        if buffersize is None:
            buffersize = self.socket_bufsize
        res = self.__read__(buffersize)
        return ret_type(res)

    def write_file(self, filename: str):
        f = open(filename)
        file_data = f.read()
        self.__write__(bytes(file_data))
        f.close()

    def read_file(self, buffer_file: str):
        buffer = open(buffer_file)
        file_data = self.__read__(self.socket_bufsize)
        file_text = file_data.decode(encoding=self.socket_encoding)
        buffer.write(file_text)
        buffer.close()


class SimpleSocket(_Sock):
    def __init__(self):
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, data: str) -> int:
        return self.write(data)

    def receive(self) -> str:
        data: bytes = self.read()
        return data.decode(self.socket_encoding)

    def send_file(self, file: str) -> int:
        return self.send_file(file)

    def receive_file(self, buffer: str) -> None:
        self.read_file(buffer)


SocketStream = _Sock

AF_INET = property(lambda: int(socket.AF_INET))
SOCK_STREAM = property(lambda: int(socket.SOCK_STREAM))
