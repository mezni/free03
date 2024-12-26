package boltstore

import (
	"fmt"

	"github.com/boltdb/bolt"
)

type BoltDBManager struct {
	db *bolt.DB
}

// NewBoltDBManager creates and initializes a new BoltDBManager
func NewBoltDBManager(dbPath string, buckets []string) (*BoltDBManager, error) {
	// Open the BoltDB database
	db, err := bolt.Open(dbPath, 0600, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to open database: %w", err)
	}

	// Initialize the buckets
	err = db.Update(func(tx *bolt.Tx) error {
		for _, bucket := range buckets {
			_, err := tx.CreateBucketIfNotExists([]byte(bucket))
			if err != nil {
				return fmt.Errorf("failed to create bucket '%s': %w", bucket, err)
			}
		}
		return nil
	})
	if err != nil {
		_ = db.Close()
		return nil, fmt.Errorf("failed to initialize buckets: %w", err)
	}

	return &BoltDBManager{db: db}, nil
}

// GetDB returns the underlying BoltDB instance
func (m *BoltDBManager) GetDB() *bolt.DB {
	return m.db
}

// Close closes the database connection
func (m *BoltDBManager) Close() error {
	return m.db.Close()
}
