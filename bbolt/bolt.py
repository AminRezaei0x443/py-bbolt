from ctypes import c_int, c_ulong, c_char_p, c_long, c_void_p, string_at, byref, cdll
from distutils.sysconfig import get_config_var
from pathlib import Path


class BoltDB:
    typeDefs = {
        "openDatabase":{
            "args": [c_char_p],
            "rt": c_long,
        },
        "currentError":{
            "args": [],
            "rt": c_char_p,
        },
        "putBKV":{
            "args": [c_ulong, c_char_p, c_char_p, c_char_p, c_int],
            "rt": c_int,
        },
        "getBK":{
            "args": [c_ulong, c_char_p, c_char_p, c_void_p],
            "rt": c_void_p,
        },
        "closeDatabase":{
            "args": [c_ulong],
            "rt": c_int,
        },
        "freeP":{
            "args": [c_void_p]
        }
    }

    def __init__(self):
        p = Path(__file__).absolute().parent.parent
        so_file = p / ('_bbolt_go' + get_config_var("EXT_SUFFIX"))
        print("loading", so_file)
        bolt = cdll.LoadLibrary(so_file)
        for k in BoltDB.typeDefs:
            v = BoltDB.typeDefs[k]
            func = getattr(bolt, k)
            func.argtypes = v["args"]
            if "rt" in v:
                func.restype = v["rt"]
            setattr(self, f"_{k}", func)
    
    def _err(self):
        e = self._currentError()
        if e is None:
            return None
        v = string_at(e)
        self._freeP(e)
        return v

    def _rerr(self):
        e = self._err()
        if e is None:
            e = "unk err"
        raise RuntimeError(f"bolt error: {e}")

    def _ensureHandle(self):
        handle = getattr(self, "_handle", -1)
        if handle == -1:
            raise RuntimeError("bolt: database not open")
        return handle

    def open(self, path):
        t = self._openDatabase(path.encode("utf-8"))
        if t == 0:
            self._rerr()
        setattr(self, "_handle", t)
    
    def put(self, bucket, key, value):
        handle = self._ensureHandle()
        b = bucket.encode("utf-8")
        k = key.encode("utf-8")
        if not isinstance(value, bytes):
            if isinstance(value, str):
                v = bytes(value, "utf-8")
            else:
                v = bytes(value)
        else:
            v = value
        res = self._putBKV(handle, b, k, v, len(v))
        if res == 0:
            self._rerr()
    
    def get(self, bucket, key):
        handle = self._ensureHandle()
        b = bucket.encode("utf-8")
        k = key.encode("utf-8")
        vLen = c_int(0)
        res = self._getBK(handle, b, k, byref(vLen))
        if vLen == -1:
            self._rerr()
        value = string_at(res, vLen)
        self._freeP(res)
        return value
    
    def get_raw(self, bucket, key):
        handle = self._ensureHandle()
        b = bucket.encode("utf-8")
        k = key.encode("utf-8")
        vLen = c_int(0)
        res = self._getBK(handle, b, k, byref(vLen))
        if vLen == -1:
            self._rerr()
        return res, vLen

    def free_raw(self, val):
        self._freeP(val)

    def close(self):
        handle = self._ensureHandle()
        res = self._closeDatabase(handle)
        if res == 0:
            self._rerr()
        delattr(self, "_handle")
