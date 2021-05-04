from multi_tools.stdio import text_io

def file(file_: str):
    """
    Open file <file_> for reading and writing,
    without the system considering it as open by
    the actual process.
    """
    return text_io.TextIO(file_)


def nfile(path: str):
    """
    Create a new file as per path <path>.
    """
    try:
        x = open(path, mode="x")
        x.close()
    except:
        raise
