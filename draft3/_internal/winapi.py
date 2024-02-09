import ctypes
from ctypes import wintypes


class IMAGE_FILE_HEADER(ctypes.Structure):
    _fields_ = (
        ("_machine", wintypes.WORD),
        ("_number_of_sections", wintypes.WORD),
        ("_time_date_stamp", wintypes.DWORD),
        ("_pointer_to_symbol_table", wintypes.DWORD),
        ("_number_of_symbols", wintypes.DWORD),
        ("_size_of_optional_header", wintypes.WORD),
        ("_characteristics", wintypes.WORD),
    )


class IMAGE_DATA_DIRECTORY(ctypes.Structure):
    _fields_ = (
        ("_VirtualAddress", wintypes.DWORD),
        ("_Size", wintypes.DWORD),
    )

    @property
    def virtual_address(self):
        return self._VirtualAddress


class IMAGE_OPTIONAL_HEADER(ctypes.Structure):
    _fields_ = (
        ("_Magic", wintypes.WORD),
        ("_MajorLinkerVersion", wintypes.BYTE),
        ("_MinorLinkerVersion", wintypes.BYTE),
        ("_SizeOfCode", wintypes.DWORD),
        ("_SizeOfInitializedData", wintypes.DWORD),
        ("_SizeOfUninitializedData", wintypes.DWORD),
        ("_AddressOfEntryPoint", wintypes.DWORD),
        ("_BaseOfCode", wintypes.DWORD),
        ("_ImageBase", ctypes.c_ulonglong),
        ("_SectionAlignment", wintypes.DWORD),
        ("_FileAlignment", wintypes.DWORD),
        ("_MajorOperatingSystemVersion", wintypes.WORD),
        ("_MinorOperatingSystemVersion", wintypes.WORD),
        ("_MajorImageVersion", wintypes.WORD),
        ("_MinorImageVersion", wintypes.WORD),
        ("_MajorSubsystemVersion", wintypes.WORD),
        ("_MinorSubsystemVersion", wintypes.WORD),
        ("_Win32VersionValue", wintypes.DWORD),
        ("_SizeOfImage", wintypes.DWORD),
        ("_SizeOfHeaders", wintypes.DWORD),
        ("_CheckSum", wintypes.DWORD),
        ("_Subsystem", wintypes.WORD),
        ("_DllCharacteristics", wintypes.WORD),
        ("_SizeOfStackReserve", ctypes.c_ulonglong),
        ("_SizeOfStackCommit", ctypes.c_ulonglong),
        ("_SizeOfHeapReserve", ctypes.c_ulonglong),
        ("_SizeOfHeapCommit", ctypes.c_ulonglong),
        ("_LoaderFlags", wintypes.DWORD),
        ("_NumberOfRvaAndSizes", wintypes.DWORD),
        ("_DataDirectory", IMAGE_DATA_DIRECTORY * 16),
    )

    @property
    def data_directory(self):
        return self._DataDirectory


class IMAGE_NT_HEADERS(ctypes.Structure):
    _fields_ = (
        ("_signature", wintypes.DWORD),
        ("_file_header", IMAGE_FILE_HEADER),
        ("_optional_header", IMAGE_OPTIONAL_HEADER),
    )

    @property
    def optional_header(self) -> IMAGE_OPTIONAL_HEADER:
        return self._optional_header

PIMAGE_NT_HEADERS = ctypes.POINTER(IMAGE_NT_HEADERS)


class IMAGE_DOS_HEADER(ctypes.Structure):
    _fields_ = (
        ("_e_magic", wintypes.WORD),
        ("_e_cblp", wintypes.WORD),
        ("_e_cp", wintypes.WORD),
        ("_e_crlc", wintypes.WORD),
        ("_e_cparhdr", wintypes.WORD),
        ("_e_minalloc", wintypes.WORD),
        ("_e_maxalloc", wintypes.WORD),
        ("_e_ss", wintypes.WORD),
        ("_e_sp", wintypes.WORD),
        ("_e_csum", wintypes.WORD),
        ("_e_ip", wintypes.WORD),
        ("_e_cs", wintypes.WORD),
        ("_e_lfarlc", wintypes.WORD),
        ("_e_ovno", wintypes.WORD),
        ("_e_res", wintypes.WORD * 4),
        ("_e_oemid", wintypes.WORD),
        ("_e_oeminfo", wintypes.WORD),
        ("_e_res2", wintypes.WORD * 10),
        ("_e_lfanew", wintypes.LONG),
    )
    @property
    def e_lfanew(self):
        return self._e_lfanew

PIMAGE_DOS_HEADER = ctypes.POINTER(IMAGE_DOS_HEADER)


class IMAGE_EXPORT_DIRECTORY(ctypes.Structure):
    _fields_ = (
        ("_Characteristics", wintypes.DWORD),
        ("_TimeDateStamp", wintypes.DWORD),
        ("_MajorVersion", wintypes.WORD),
        ("_MinorVersion", wintypes.WORD),
        ("_Name", wintypes.DWORD),
        ("_Base", wintypes.DWORD),
        ("_NumberOfFunctions", wintypes.DWORD),
        ("_NumberOfNames", wintypes.DWORD),
        ("_AddressOfFunctions", wintypes.DWORD),
        ("_AddressOfNames", wintypes.DWORD),
        ("_AddressOfNameOrdinals", wintypes.DWORD),
    )

    @property
    def address_of_names(self):
        return self._AddressOfNames

    @property
    def number_of_names(self):
        return self._NumberOfNames


class RVA:
    def __init__(self, addr):
        self._addr = addr

    def _is_shorter_than8(self):
        _num = ctypes.c_long.from_address(self._addr)
        return _num.value != 0

    def get(self, base=0):
        if self._is_shorter_than8():
            return ctypes.cast(self._addr, ctypes.c_char_p).value
        return ctypes.c_char_p.from_address(self._addr + 4 + base)

PIMAGE_EXPORT_DIRECTORY = ctypes.POINTER(IMAGE_EXPORT_DIRECTORY)


PSTR = ctypes.POINTER(ctypes.c_char_p)

print(ctypes.sizeof(IMAGE_EXPORT_DIRECTORY))


def _load_lib_no_resolve(name) -> int:
    import _ctypes
    return _ctypes.LoadLibrary(name, 1)


def parse_binary_symbols(name):
    hModule = _load_lib_no_resolve(name)
    pHeader = ctypes.cast(hModule + ctypes.cast(hModule, PIMAGE_DOS_HEADER).contents.e_lfanew, PIMAGE_NT_HEADERS)
    exports = ctypes.cast(hModule + pHeader.contents.optional_header.data_directory[0].virtual_address, PIMAGE_EXPORT_DIRECTORY)
    names = ctypes.cast(exports.contents.address_of_names, ctypes.POINTER(ctypes.c_void_p))
    print(pHeader.contents.optional_header._NumberOfRvaAndSizes)



parse_binary_symbols("kernel32.dll")