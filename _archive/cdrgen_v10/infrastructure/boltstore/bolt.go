package boltstore

import (
	"encoding/json"
	"fmt"
	"go.etcd.io/bbolt"
)

// BoltPersistenceService is a service for managing BoltDB operations.
type BoltPersistenceService struct {
	DB *bbolt.DB
}

// NewBoltPersistenceService creates a new instance of BoltPersistenceService.
func NewBoltPersistenceService(db *bbolt.DB) *BoltPersistenceService {
	return &BoltPersistenceService{
		DB: db,
	}
}

// OpenDB opens the BoltDB database file at the provided file path.
func (b *BoltPersistenceService) OpenDB(filePath string) error {
	if b.DB != nil {
		// Check if the DB is already open
		return fmt.Errorf("database is already open")
	}

	var err error
	b.DB, err = bbolt.Open(filePath, 0600, nil)
	if err != nil {
		return fmt.Errorf("could not open database: %v", err)
	}
	return nil
}

// CloseDB closes the BoltDB database if it is open.
func (b *BoltPersistenceService) CloseDB() error {
	if b.DB != nil {
		return b.DB.Close()
	}
	return fmt.Errorf("database is not open")
}

// SaveListToDB saves a list of entities to the database under the specified bucket and key.
func (b *BoltPersistenceService) SaveListToDB(bucketName string, dataList interface{}, key string) error {
	if dataList == nil {
		return fmt.Errorf("dataList cannot be nil")
	}
	if bucketName == "" || key == "" {
		return fmt.Errorf("bucketName and key must not be empty")
	}

	err := b.DB.Update(func(tx *bbolt.Tx) error {
		// Create or get the bucket
		bucket, err := tx.CreateBucketIfNotExists([]byte(bucketName))
		if err != nil {
			return fmt.Errorf("could not create or access bucket '%s': %v", bucketName, err)
		}

		// Marshal the data list into JSON
		jsonData, err := json.Marshal(dataList)
		if err != nil {
			return fmt.Errorf("could not marshal data to JSON: %v", err)
		}

		// Save the data under the provided key
		if err := bucket.Put([]byte(key), jsonData); err != nil {
			return fmt.Errorf("could not save data under key '%s': %v", key, err)
		}

		return nil
	})

	return err
}

// ReadListFromDB retrieves all key-value pairs in the specified bucket and returns them as a map.
func (b *BoltPersistenceService) ReadListFromDB(bucketName string) (map[string]interface{}, error) {
	entries := make(map[string]interface{})

	err := b.DB.View(func(tx *bbolt.Tx) error {
		// Get the bucket
		bucket := tx.Bucket([]byte(bucketName))
		if bucket == nil {
			return fmt.Errorf("bucket '%s' does not exist", bucketName)
		}

		// Iterate over the keys and their values in the bucket
		return bucket.ForEach(func(k, v []byte) error {
			var value interface{}
			if err := json.Unmarshal(v, &value); err != nil {
				return fmt.Errorf("could not unmarshal value for key '%s': %v", k, err)
			}
			entries[string(k)] = value
			return nil // returning nil continues the iteration
		})
	})

	return entries, err
}
