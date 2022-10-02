package bolt_ffi

import (
	"errors"

	bolt "go.etcd.io/bbolt"
)

type BoltDB struct {
	_db *bolt.DB
}

func OpenDB(path string) (*BoltDB, error) {
	db, err := bolt.Open(path, 0666, nil)
	return &BoltDB{_db: db}, err
}

func (b *BoltDB) Close() error {
	return b._db.Close()
}

func (b *BoltDB) Get(bucket string, key string) ([]byte, error) {
	var res []byte
	e := b._db.View(func(tx *bolt.Tx) error {
		buk := tx.Bucket([]byte(bucket))
		if buk == nil {
			return errors.New("bucket doesn't exist")
		}
		res = buk.Get([]byte(key))
		return nil
	})
	if e != nil {
		return nil, e
	}
	return res, nil
}

func (b *BoltDB) Set(bucket string, key string, value []byte) error {
	e := b._db.Update(func(tx *bolt.Tx) error {
		buk, e := tx.CreateBucketIfNotExists([]byte(bucket))
		if e != nil {
			return e
		}
		return buk.Put([]byte(key), value)
	})
	return e
}

func (b *BoltDB) CreateBucket(bucket string) error {
	e := b._db.Update(func(tx *bolt.Tx) error {
		_, e := tx.CreateBucketIfNotExists([]byte(bucket))
		if e != nil {
			return e
		}
		return nil
	})
	return e
}
