package boltstore

import (
	"encoding/json"
	"errors"
	"log"
	"sync"
	"time"

	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/domain/entities" // Import the entities package
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
	return manager.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte(bucketName))
		if bucket == nil {
			return bolt.ErrBucketNotFound
		}
		return fn(tx, bucket)
	})
}

// LoadList saves a list of generic entities into the specified bucket.
func (manager *BoltDBManager[T]) LoadList(bucketName string, list []T, getKey func(item T) string, checkDuplicateColumns []string, getMaxID func(item T) int) error {
	return manager.WithTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		for _, item := range list {
			// Check for duplicates
			if err := checkDuplicate(bucket, checkDuplicateColumns, item); err != nil {
				return err
			}

			// Get the max ID and update the entity ID
			maxID, err := manager.GetMaxID(bucketName, getMaxID)
			if err != nil {
				return err
			}

			// Directly update the item ID without using setItemID
			itemID := maxID + 1
			switch v := any(&item).(type) {
			case *entities.NetworkTechnology:
				v.ID = itemID
			}

			// Store the item
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

// GetMaxID fetches the maximum ID from the items in the bucket based on the provided function.
func (manager *BoltDBManager[T]) GetMaxID(bucketName string, getID func(item T) int) (int, error) {
	var maxID int

	// Use WithReadOnlyTransaction to access the bucket and iterate over its items.
	err := manager.WithReadOnlyTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		// If the bucket is nil, return no error, and maxID should remain 0.
		if bucket == nil {
			return nil // Return nil instead of an error.
		}

		// Iterate over all the items in the bucket and find the maximum ID.
		return bucket.ForEach(func(k, v []byte) error {
			var item T
			if err := json.Unmarshal(v, &item); err != nil {
				return err
			}
			id := getID(item)
			if id > maxID {
				maxID = id
			}
			return nil
		})
	})

	// If there was an error (other than bucket not being found), return that error.
	if err != nil && err.Error() != "bucket not found" {
		return 0, err
	}

	// Return the maxID (which could still be 0 if no items were found).
	return maxID, nil
}

// checkDuplicate checks for duplicates based on the specified columns and item.
func checkDuplicate[T any](bucket *bolt.Bucket, checkDuplicateColumns []string, item T) error {
	// Check for duplicates based on the specified columns.
	// In this example, we only check the "Name" column for duplicates.
	for _, column := range checkDuplicateColumns {
		if column == "Name" {
			// If "Name" is a column to check, we perform the check.
			itemName := getName(item)
			cursor := bucket.Cursor()
			for k, v := cursor.Seek([]byte(itemName)); k != nil; k, v = cursor.Next() {
				var existingItem T
				if err := json.Unmarshal(v, &existingItem); err != nil {
					return err
				}
				if getName(existingItem) == itemName {
					// Duplicate found, skip insertion
					log.Printf("Duplicate found for item: %+v, skipping insertion.", item)
					return nil // Returning nil here to skip the item
				}
			}
		}
	}
	return nil
}

// getName is a helper function to extract the "Name" field from the item.
func getName[T any](item T) string {
	// Assuming the item has a `Name` field. You might need to adjust this
	// if `T` has a different structure.
	switch v := any(item).(type) {
	case entities.NetworkTechnology:
		return v.Name
	default:
		return ""
	}
}