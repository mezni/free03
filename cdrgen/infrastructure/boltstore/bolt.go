package boltstore

import (
	"encoding/json"
	"fmt"
	"go.etcd.io/bbolt"
)

// BoltDBConfig holds the configuration for BoltDB operations.
type BoltDBConfig struct {
	DBName     string
	BucketName string
}

// withDB abstracts the repetitive BoltDB open and close operations.
func (config *BoltDBConfig) withDB(callback func(db *bbolt.DB) error) error {
	db, err := bbolt.Open(config.DBName, 0666, nil)
	if err != nil {
		return fmt.Errorf("failed to open BoltDB: %v", err)
	}
	defer db.Close()

	return callback(db)
}

// getOrCreateBucket retrieves or creates a bucket within a transaction.
func getOrCreateBucket(tx *bbolt.Tx, bucketName string) (*bbolt.Bucket, error) {
	bucket, err := tx.CreateBucketIfNotExists([]byte(bucketName))
	if err != nil {
		return nil, fmt.Errorf("failed to create or access bucket: %v", err)
	}
	return bucket, nil
}

// extractID extracts the "ID" field from a map and ensures it's a string.
func extractID(item map[string]interface{}) (string, error) {
	idValue, exists := item["ID"]
	if !exists {
		return "", fmt.Errorf("missing ID field in data item")
	}

	idStr, ok := idValue.(string)
	if !ok {
		return "", fmt.Errorf("ID field must be a string")
	}

	return idStr, nil
}

// saveItemToBucket saves a single item to a given bucket.
func saveItemToBucket(bucket *bbolt.Bucket, id string, item map[string]interface{}) error {
	itemData, err := json.Marshal(item)
	if err != nil {
		return fmt.Errorf("failed to marshal item with ID %s: %v", id, err)
	}

	err = bucket.Put([]byte(id), itemData)
	if err != nil {
		return fmt.Errorf("failed to save item with ID %s to bucket: %v", id, err)
	}

	return nil
}

// retrieveItemsFromBucket retrieves all items from a given bucket.
func retrieveItemsFromBucket(bucket *bbolt.Bucket) ([]map[string]interface{}, error) {
	var data []map[string]interface{}

	err := bucket.ForEach(func(k, v []byte) error {
		var item map[string]interface{}
		if err := json.Unmarshal(v, &item); err != nil {
			return fmt.Errorf("failed to unmarshal item with key %s: %v", k, err)
		}
		data = append(data, item)
		return nil
	})

	return data, err
}

// SaveToBoltDB saves a list of maps to BoltDB using the specified configuration.
func SaveToBoltDB(config BoltDBConfig, data []map[string]interface{}) error {
	return config.withDB(func(db *bbolt.DB) error {
		return db.Update(func(tx *bbolt.Tx) error {
			bucket, err := getOrCreateBucket(tx, config.BucketName)
			if err != nil {
				return err
			}

			for _, item := range data {
				id, err := extractID(item)
				if err != nil {
					return err
				}
				if err := saveItemToBucket(bucket, id, item); err != nil {
					return err
				}
			}

			return nil
		})
	})
}

// ReadFromBoltDB reads a list of maps from BoltDB using the specified configuration.
func ReadFromBoltDB(config BoltDBConfig) ([]map[string]interface{}, error) {
	var data []map[string]interface{}

	err := config.withDB(func(db *bbolt.DB) error {
		return db.View(func(tx *bbolt.Tx) error {
			bucket := tx.Bucket([]byte(config.BucketName))
			if bucket == nil {
				return fmt.Errorf("bucket %s not found", config.BucketName)
			}

			items, err := retrieveItemsFromBucket(bucket)
			if err != nil {
				return err
			}
			data = items
			return nil
		})
	})

	return data, err
}
