import sys


class stdin:
    """
    Contains only the useful functions of sys.stdin.
    """

    @staticmethod
    def read() -> str:
        return sys.stdin.read()

    @staticmethod
    def fileno() -> int:
        return sys.stdin.fileno()

    @staticmethod
    def seek(offset: int):
        return sys.stdin.seek(offset)


class stdout:
    """
    Contains only the useful functions of sys.stdout.
    """

    @staticmethod
    def write(text: str) -> None:
        sys.stdout.write(text)

    @staticmethod
    def fileno() -> int:
        return sys.stdout.fileno()

    @staticmethod
    def seek(offset: int):
        return sys.stdout.seek(offset)


class stderr:
    """
    Contains only the useful functions of sys.stderr.
    """

    @staticmethod
    def write(text: str) -> None:
        sys.stderr.write(text)

    @staticmethod
    def fileno() -> int:
        return sys.stderr.fileno()

    @staticmethod
    def seek(offset: int):
        return sys.stderr.seek(offset)
