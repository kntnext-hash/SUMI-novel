"""Replace icon resources in a newly copied Windows launcher (stdlib only).

Uses Microsoft's BeginUpdateResource/UpdateResource/EndUpdateResource APIs.
Never pass the source runtime: the build owns and modifies its output copy.
"""
import ctypes as C
from ctypes import wintypes as W
import os
import struct


def resources(path):
    """Read resource bytes without executing the PE module."""
    api = C.WinDLL("kernel32", use_last_error=True)
    api.LoadLibraryExW.argtypes = [W.LPCWSTR, W.HANDLE, W.DWORD]
    api.LoadLibraryExW.restype = W.HMODULE
    api.FreeLibrary.argtypes = [W.HMODULE]
    api.FindResourceExW.argtypes = [W.HMODULE, C.c_void_p, C.c_void_p, W.WORD]
    api.FindResourceExW.restype = W.HANDLE
    api.SizeofResource.argtypes = [W.HMODULE, W.HANDLE]
    api.SizeofResource.restype = W.DWORD
    api.LoadResource.argtypes = [W.HMODULE, W.HANDLE]
    api.LoadResource.restype = W.HANDLE
    api.LockResource.argtypes = [W.HANDLE]
    api.LockResource.restype = C.c_void_p
    type_cb = C.WINFUNCTYPE(W.BOOL, W.HMODULE, C.c_void_p, C.c_ssize_t)
    name_cb = C.WINFUNCTYPE(W.BOOL, W.HMODULE, C.c_void_p, C.c_void_p, C.c_ssize_t)
    lang_cb = C.WINFUNCTYPE(W.BOOL, W.HMODULE, C.c_void_p, C.c_void_p, W.WORD, C.c_ssize_t)
    api.EnumResourceTypesW.argtypes = [W.HMODULE, type_cb, C.c_ssize_t]
    api.EnumResourceNamesW.argtypes = [W.HMODULE, C.c_void_p, name_cb, C.c_ssize_t]
    api.EnumResourceLanguagesW.argtypes = [W.HMODULE, C.c_void_p, C.c_void_p, lang_cb, C.c_ssize_t]
    result = {}
    def identifier(value):
        value = value or 0
        return value if value <= 65535 else C.wstring_at(value)
    @lang_cb
    def language(module, kind, name, lang, unused):
        entry = api.FindResourceExW(module, kind, name, lang)
        size = api.SizeofResource(module, entry)
        pointer = api.LockResource(api.LoadResource(module, entry))
        result[(identifier(kind), identifier(name), lang)] = C.string_at(pointer, size)
        return True
    @name_cb
    def name(module, kind, key, unused):
        return api.EnumResourceLanguagesW(module, kind, key, language, 0)
    @type_cb
    def kind(module, key, unused):
        return api.EnumResourceNamesW(module, key, name, 0)
    module = api.LoadLibraryExW(str(path), None, 2)  # LOAD_LIBRARY_AS_DATAFILE
    if not module:
        raise C.WinError(C.get_last_error())
    try:
        if not api.EnumResourceTypesW(module, kind, 0):
            raise C.WinError(C.get_last_error())
    finally:
        api.FreeLibrary(module)
    return result


def replace_icon(executable, icon):
    if os.name != "nt":
        raise RuntimeError("Windows distribution icon embedding requires Windows.")
    data = icon.read_bytes()
    reserved, kind, count = struct.unpack_from("<HHH", data)
    if reserved or kind != 1 or not 0 < count <= 256:
        raise ValueError("Invalid ICO header")
    group = data[:6]
    images = {}
    for index in range(count):
        entry = data[6 + 16 * index:22 + 16 * index]
        size, offset = struct.unpack_from("<II", entry, 8)
        if not size or offset < 6 + 16 * count or offset + size > len(data):
            raise ValueError("Invalid ICO image range")
        images[index + 1] = data[offset:offset + size]
        group += entry[:12] + struct.pack("<H", index + 1)
    before = resources(executable)
    api = C.WinDLL("kernel32", use_last_error=True)
    api.BeginUpdateResourceW.argtypes = [W.LPCWSTR, W.BOOL]
    api.BeginUpdateResourceW.restype = W.HANDLE
    api.UpdateResourceW.argtypes = [W.HANDLE, C.c_void_p, C.c_void_p, W.WORD, C.c_void_p, W.DWORD]
    api.EndUpdateResourceW.argtypes = [W.HANDLE, W.BOOL]
    handle = api.BeginUpdateResourceW(str(executable), False)
    if not handle:
        raise C.WinError(C.get_last_error())
    def put(kind, name, lang, payload):
        key = C.c_void_p(name) if isinstance(name, int) else C.cast(C.c_wchar_p(name), C.c_void_p)
        buffer = C.create_string_buffer(payload) if payload is not None else None
        if not api.UpdateResourceW(handle, C.c_void_p(kind), key, lang, buffer, len(payload) if payload else 0):
            raise C.WinError(C.get_last_error())
    try:
        for (kind, name, lang) in before:
            if kind in (3, 14):
                put(kind, name, lang, None)
        for name, payload in images.items():
            put(3, name, 0, payload)
        put(14, 1, 0, group)
    except BaseException:
        api.EndUpdateResourceW(handle, True)
        raise
    if not api.EndUpdateResourceW(handle, False):
        raise C.WinError(C.get_last_error())
    expected = {key: value for key, value in before.items() if key[0] not in (3, 14)}
    expected.update({(3, name, 0): value for name, value in images.items()})
    expected[(14, 1, 0)] = group
    if resources(executable) != expected:
        raise ValueError("Embedded icons or preserved non-icon resources differ from expected bytes")
    return {"images": count, "non_icon_resources_preserved": len(expected) - count - 1}
