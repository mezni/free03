package boltstore

import (
	"log"
	"sync"
	"time"

	"github.com/boltdb/bolt"
)

type BoltDBManager struct {
	db *bolt.DB
	mu sync.Mutex
}

// NewBoltDBManager initializes a new BoltDB instance
func NewBoltDBManager(filePath string, timeout time.Duration) (*BoltDBManager, error) {
	db, err := bolt.Open(filePath, 0600, &bolt.Options{Timeout: timeout})
	if err != nil {
		return nil, err
	}

	manager := &BoltDBManager{
		db: db,
	}
	return manager, nil
}

// Close safely closes the BoltDB instance
func (manager *BoltDBManager) Close() {
	manager.mu.Lock()
	defer manager.mu.Unlock()
	if err := manager.db.Close(); err != nil {
		log.Println("Error closing BoltDB:", err)
	}
}

// WithTransaction provides a BoltDB transaction (read/write)
func (manager *BoltDBManager) WithTransaction(bucketName string, fn func(tx *bolt.Tx, bucket *bolt.Bucket) error) error {
	manager.mu.Lock()
	defer manager.mu.Unlock()

	return manager.db.Update(func(tx *bolt.Tx) error {
		bucket, err := tx.CreateBucketIfNotExists([]byte(bucketName))
		if err != nil {
			return err
		}
		return fn(tx, bucket)
	})
}

// WithReadOnlyTransaction provides a read-only BoltDB transaction
func (manager *BoltDBManager) WithReadOnlyTransaction(bucketName string, fn func(tx *bolt.Tx, bucket *bolt.Bucket) error) error {
	manager.mu.Lock()
	defer manager.mu.Unlock()

	return manager.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte(bucketName))
		if bucket == nil {
			return bolt.ErrBucketNotFound
		}
		return fn(tx, bucket)
	})
}
