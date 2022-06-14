package core

type ObjectStore struct {
	objs map[uint64]interface{}
	size uint64
}

var globalStore *ObjectStore

func init() {
	globalStore = &ObjectStore{
		size: 0,
		objs: make(map[uint64]interface{}),
	}
}

func AppendObject(obj interface{}) uint64 {
	globalStore.size++
	k := globalStore.size
	globalStore.objs[k] = obj
	return k
}

func GetObject(key uint64) interface{} {
	return globalStore.objs[key]
}

func RemoveObject(key uint64) {
	delete(globalStore.objs, key)
}
