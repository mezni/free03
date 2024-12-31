package boltstore

import (
	"encoding/json"
	"errors"
	"fmt"
	"go.etcd.io/bbolt"
)

// BoltDBConfig holds the configuration for BoltDB operations.
type BoltDBConfig struct {
	db *bbolt.DB // The internal reference to the database instance
}

// NewBoltDBConfig initializes and returns a new instance of BoltDBConfig.
func NewBoltDBConfig() *BoltDBConfig {
	return &BoltDBConfig{}
}

// Open opens the database file with the given path.
func (cfg *BoltDBConfig) Open(dbPath string) error {
	// Open the database file with read-write permissions
	db, err := bbolt.Open(dbPath, 0600, nil)
	if err != nil {
		return fmt.Errorf("error opening database: %w", err)
	}
	cfg.db = db
	return nil
}

// Create creates the database file if it does not exist and opens it.
func (cfg *BoltDBConfig) Create(dbPath string) error {
	// Check if the database file already exists
	db, err := bbolt.Open(dbPath, 0600, nil)
	if err != nil {
		return fmt.Errorf("error creating/opening database: %w", err)
	}
	cfg.db = db
	return nil
}

// Close safely closes the database when done.
func (cfg *BoltDBConfig) Close() error {
	// Ensure the database is not nil and can be closed safely
	if cfg.db == nil {
		return errors.New("no database connection to close")
	}

	// Close the database connection
	if err := cfg.db.Close(); err != nil {
		return fmt.Errorf("error closing database: %w", err)
	}

	cfg.db = nil
	return nil
}

// SaveToBoltDB saves the provided data to the specified bucket in the database.
func (cfg *BoltDBConfig) SaveToBoltDB(bucketName string, dataAsMaps []map[string]interface{}) error {
	if cfg.db == nil {
		return errors.New("database not open")
	}

	// Start a write transaction
	return cfg.db.Update(func(tx *bbolt.Tx) error {
		// Create or retrieve the bucket
		bucket, err := tx.CreateBucketIfNotExists([]byte(bucketName))
		if err != nil {
			return fmt.Errorf("error creating/retrieving bucket: %w", err)
		}

		// Iterate over the data and save each item
		for _, item := range dataAsMaps {
			id, err := extractID(item)
			if err != nil {
				return fmt.Errorf("error extracting ID: %w", err)
			}

			// Save the item to the bucket
			if err := saveItemToBucket(bucket, id, item); err != nil {
				return fmt.Errorf("error saving item to bucket: %w", err)
			}
		}

		return nil
	})
}

// extractID is a utility function to extract the ID from a map.
func extractID(item map[string]interface{}) (string, error) {
	// Assuming the item has an "ID" key.
	id, ok := item["ID"].(string)
	if !ok {
		return "", errors.New("ID field missing or invalid")
	}
	return id, nil
}

// saveItemToBucket saves a single item to the bucket.
func saveItemToBucket(bucket *bbolt.Bucket, id string, item map[string]interface{}) error {
	// Assuming you're saving the data as JSON or some other format
	data, err := json.Marshal(item)
	if err != nil {
		return fmt.Errorf("error marshalling item: %w", err)
	}

	// Save the item under its ID
	if err := bucket.Put([]byte(id), data); err != nil {
		return fmt.Errorf("error saving data to bucket: %w", err)
	}

	return nil
}
