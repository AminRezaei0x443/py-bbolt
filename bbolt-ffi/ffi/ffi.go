//+build linux darwin windows

package main

// #include <stdlib.h>
import "C"
import (
	bolt_ffi "bolt-ffi"
	"bolt-ffi/core"
	"unsafe"
)

var _globalError error

//export currentError
func currentError() *C.char {
	if _globalError == nil {
		return nil
	}
	return C.CString(_globalError.Error())
}

//export openDatabase
func openDatabase(path *C.char) C.ulong {
	gPath := C.GoString(path)
	db, e := bolt_ffi.OpenDB(gPath)
	if e != nil {
		_globalError = e
		return 0
	}
	return C.ulong(core.AppendObject(db))
}

//export putBKV
func putBKV(dbHandle C.ulong, bucket *C.char, key *C.char, value *C.char, valueLen C.int) C.int {
	db := (core.GetObject(uint64(dbHandle))).(*bolt_ffi.BoltDB)
	v := C.GoBytes(unsafe.Pointer(value), valueLen)
	e := db.Set(C.GoString(bucket), C.GoString(key), v)
	if e != nil {
		_globalError = e
		return 0
	}
	return 1
}

//export getBK
func getBK(dbHandle C.ulong, bucket *C.char, key *C.char, size unsafe.Pointer) unsafe.Pointer {
	db := (core.GetObject(uint64(dbHandle))).(*bolt_ffi.BoltDB)
	v, e := db.Get(C.GoString(bucket), C.GoString(key))
	s := (*C.int)(size)
	if e != nil {
		_globalError = e
		*s = -1
		return nil
	}
	*s = C.int(len(v))
	ptr := C.CBytes(v)
	return ptr
}

//export createBucket
func createBucket(dbHandle C.ulong, bucket *C.char) C.int {
	db := (core.GetObject(uint64(dbHandle))).(*bolt_ffi.BoltDB)
	e := db.CreateBucket(C.GoString(bucket))
	if e != nil {
		_globalError = e
		return 0
	}
	return 1
}

//export closeDatabase
func closeDatabase(dbHandle C.ulong) C.int {
	db := (core.GetObject(uint64(dbHandle))).(*bolt_ffi.BoltDB)
	e := db.Close()
	if e != nil {
		_globalError = e
		return 0
	}
	return 1
}

//export freeP
func freeP(p unsafe.Pointer) {
	C.free(p)
}

func main() {

}
