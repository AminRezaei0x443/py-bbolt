package bolt_ffi

import "testing"

func TestBolt(t *testing.T) {
	db, e := OpenDB(".tmp/x.db")
	if e != nil{
		t.Error(e)
	}
	e = db.Set("x", "v", []byte{1,2,100,22,142})
	if e != nil{
		t.Error(e)
	}
	e = db.Close()
	if e != nil{
		t.Error(e)
	}
	db, e = OpenDB(".tmp/x.db")
	if e != nil{
		t.Error(e)
	}
	v, e := db.Get("x", "v")
	if e != nil{
		t.Error(e)
	}
	t.Log(v)
}

func TestBolt2(t *testing.T) {
	db, e := OpenDB(".tmp/test.idb")
	if e != nil{
		t.Error(e)
	}
	v, e := db.Get("buk", "a")
	if e != nil{
		t.Error(e)
	}
	t.Log(v)
}
