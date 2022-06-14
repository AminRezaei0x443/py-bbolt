import ctypes
bolt = ctypes.cdll.LoadLibrary("./bolt.dll")
openDatabase = bolt.openDatabase
openDatabase.argtypes = [ctypes.c_char_p]
openDatabase.restype = ctypes.c_long
currentError = bolt.currentError
currentError.argtypes = []
currentError.restype = ctypes.c_char_p
t = openDatabase("./t.db".encode("utf-8"))
print(t)

putBKV = bolt.putBKV
putBKV.argtypes = [ctypes.c_ulong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int]
putBKV.restype = ctypes.c_int
bucket = "test".encode("utf-8")
k = "k".encode("utf-8")
v = bytes([1, 4, 1])
rc = putBKV(t, bucket, k, v, len(v))
print(rc)

getBK = bolt.getBK
getBK.argtypes = [ctypes.c_ulong, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_void_p]
getBK.restype = ctypes.c_char_p
vLen = ctypes.c_int(0)
k = "kx".encode("utf-8")
rc = getBK(t, bucket, k, ctypes.byref(vLen))
print(vLen)
print(type(rc))
print(ctypes.string_at(rc, vLen))

closeDatabase = bolt.closeDatabase
closeDatabase.argtypes = [ctypes.c_ulong]
closeDatabase.restype = ctypes.c_int
print(closeDatabase(t))
print(bolt.free)