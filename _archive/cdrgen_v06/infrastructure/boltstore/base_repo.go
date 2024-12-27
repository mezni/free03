package boltstore

import (
	"encoding/json"
	"fmt"
	"github.com/boltdb/bolt"
	"log"
)

// BoltRepository provides common functionalities for BoltDB repositories.
type BoltRepository struct {
	db         *bolt.DB
	bucketName string
}

// NewBoltRepository initializes a new BoltRepository with the given database path and bucket name.
func NewBoltRepository(dbPath, bucketName string) (*BoltRepository, error) {
	db, err := bolt.Open(dbPath, 0600, nil)
	if err != nil {
		return nil, fmt.Errorf("error opening database: %w", err)
	}

	// Create bucket if it doesn't exist
	err = db.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucketIfNotExists([]byte(bucketName))
		return err
	})
	if err != nil {
		return nil, fmt.Errorf("error creating bucket: %w", err)
	}

	return &BoltRepository{db: db, bucketName: bucketName}, nil
}

// Close closes the database connection.
func (r *BoltRepository) Close() {
	r.db.Close()
}

// Serialize implements the serialization logic (using JSON).
func (r *BoltRepository) Serialize(data interface{}) ([]byte, error) {
	return json.Marshal(data)
}

// Deserialize implements the deserialization logic (using JSON).
func (r *BoltRepository) Deserialize(data []byte, result interface{}) error {
	return json.Unmarshal(data, result)
}

// Create inserts a new item into the bucket.
func (r *BoltRepository) Create(itemID int, item interface{}) (int, error) {
	err := r.db.Update(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(r.bucketName))

		// Generate next available ID
		id, _ := b.NextSequence()
		itemID = int(id)

		// Serialize the item before inserting it into the bucket
		data, err := r.Serialize(item)
		if err != nil {
			return fmt.Errorf("error serializing item: %w", err)
		}

		// Store the serialized data
		return b.Put(itob(itemID), data)
	})

	if err != nil {
		log.Printf("Error creating item: %v", err)
		return 0, err
	}

	return itemID, nil
}

// Utility functions to convert between int and byte slice
func itob(v int) []byte {
	return []byte{byte(v)} // This is for small integers, extend as needed
}

func btoi(b []byte) int {
	return int(b[0]) // This is for small integers, extend as needed
}
