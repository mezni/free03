package repositories

import (
	"encoding/json"
	"fmt"
	"go.etcd.io/bbolt"
)

// BoltDBLocationRepository is a BoltDB implementation of the LocationRepository interface.
type BoltPersistenceService struct {
	DB *bbolt.DB
}

// NewBoltDBLocationRepository creates a new instance of BoltDBLocationRepository.
func NewBoltPersistenceService(db *bbolt.DB) *BoltPersistenceService {
	return &BoltPersistenceService{
		DB: db,
	}


// OpenDB opens the BoltDB database file.
func (b *BoltPersistenceService) OpenDB(filePath string) error {
	var err error
	b.DB, err = bbolt.Open(filePath, 0600, nil)
	if err != nil {
		return fmt.Errorf("could not open database: %v", err)
	}
	return nil
}

// CloseDB closes the BoltDB database.
func (b *BoltPersistenceService) CloseDB() error {
	if b.DB != nil {
		return b.DB.Close()
	}
	return nil
}

// SaveListToDB saves a list of entities to the database under the specified bucket and key.
func (b *BoltPersistenceService) SaveListToDB(bucketName string, dataList interface{}, key string) error {
	// Check if dataList is empty
	if dataList == nil {
		return fmt.Errorf("dataList cannot be nil")
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

		// Save the data using the provided key
		if err := bucket.Put([]byte(key), jsonData); err != nil {
			return fmt.Errorf("could not save data under key '%s': %v", key, err)
		}

		return nil
	})

	return err
}

// ReadListFromDB lists all key-value pairs in the specified bucket.
func (b *BoltPersistenceService) ReadListFromDB(bucketName string) (map[string]interface{}, error) {
	entries := make(map[string]interface{})

	err := b.DB.View(func(tx *bbolt.Tx) error {
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
