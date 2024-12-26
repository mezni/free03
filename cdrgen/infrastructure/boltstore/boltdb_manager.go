package boltstore

import (
	"encoding/json"
	"errors"
	"log"
	"sync"
	"time"

	"github.com/boltdb/bolt"
)

// BoltDBManager provides a thread-safe manager for BoltDB operations.
type BoltDBManager[T any] struct {
	db *bolt.DB
	mu sync.Mutex
}

// NewBoltDBManager initializes a new BoltDB instance.
func NewBoltDBManager[T any](filePath string, timeout time.Duration) (*BoltDBManager[T], error) {
	db, err := bolt.Open(filePath, 0600, &bolt.Options{Timeout: timeout})
	if err != nil {
		return nil, err
	}

	manager := &BoltDBManager[T]{
		db: db,
	}
	return manager, nil
}

// Close safely closes the BoltDB instance.
func (manager *BoltDBManager[T]) Close() {
	manager.mu.Lock()
	defer manager.mu.Unlock()
	if err := manager.db.Close(); err != nil {
		log.Println("Error closing BoltDB:", err)
	}
}

// WithTransaction provides a BoltDB transaction (read/write).
func (manager *BoltDBManager[T]) WithTransaction(bucketName string, fn func(tx *bolt.Tx, bucket *bolt.Bucket) error) error {
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

// WithReadOnlyTransaction provides a read-only BoltDB transaction.
func (manager *BoltDBManager[T]) WithReadOnlyTransaction(bucketName string, fn func(tx *bolt.Tx, bucket *bolt.Bucket) error) error {
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

// LoadList saves a list of generic entities into the specified bucket.
func (manager *BoltDBManager[T]) LoadList(bucketName string, list []T, getKey func(item T) string) error {
	return manager.WithTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		for _, item := range list {
			key := getKey(item)
			if key == "" {
				return errors.New("key cannot be empty")
			}
			data, err := json.Marshal(item)
			if err != nil {
				return err
			}
			if err := bucket.Put([]byte(key), data); err != nil {
				return err
			}
		}
		return nil
	})
}

// DumpList reads all entries from a specified bucket and returns them as a list of T.
func (manager *BoltDBManager[T]) DumpList(bucketName string) ([]T, error) {
	var result []T

	err := manager.WithReadOnlyTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		if bucket == nil {
			return errors.New("bucket not found")
		}

		return bucket.ForEach(func(k, v []byte) error {
			var item T
			if err := json.Unmarshal(v, &item); err != nil {
				return err
			}
			result = append(result, item)
			return nil
		})
	})
	return result, err
}

// GetMaxID returns the maximum ID found in the specified bucket
func (manager *BoltDBManager[T]) GetMaxID(bucketName string, getID func(item T) int) (int, error) {
	var maxID int

	err := manager.WithReadOnlyTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		if bucket == nil {
			return errors.New("bucket not found")
		}

		return bucket.ForEach(func(k, v []byte) error {
			var item T
			if err := json.Unmarshal(v, &item); err != nil {
				return err
			}

			// Get the ID of the current item and check if it is the highest
			itemID := getID(item)
			if itemID > maxID {
				maxID = itemID
			}
			return nil
		})
	})

	if err != nil {
		return 0, err
	}

	return maxID, nil
}