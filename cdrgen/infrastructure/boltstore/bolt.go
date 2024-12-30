package boltstore

import (
	"encoding/json"
	"fmt"
	"go.etcd.io/bbolt"
)

// SaveToBoltDB saves any type of data to BoltDB using a transaction.
// dbName is the name of the BoltDB database.
// bucketName is the name of the bucket in which the data will be stored.
// data is the interface{} type that allows you to store any data.
func SaveToBoltDB(dbName, bucketName string, data []interface{}) error {
	// Open or create the BoltDB database
	db, err := bbolt.Open(dbName, 0666, nil)
	if err != nil {
		return fmt.Errorf("failed to open BoltDB: %v", err)
	}
	defer db.Close()

	// Perform the transaction
	err = db.Update(func(tx *bbolt.Tx) error {
		// Create a bucket for storing the data (if it doesn't exist)
		bucket, err := tx.CreateBucketIfNotExists([]byte(bucketName))
		if err != nil {
			return fmt.Errorf("failed to create bucket: %v", err)
		}

		// Iterate through the data and save each item to the bucket
		for i, item := range data {
			// Marshal the item into JSON for storage
			itemData, err := json.Marshal(item)
			if err != nil {
				return fmt.Errorf("failed to marshal item: %v", err)
			}

			// Use the index as the key and the JSON data as the value
			err = bucket.Put([]byte(fmt.Sprintf("%d", i)), itemData)
			if err != nil {
				return fmt.Errorf("failed to save item to bucket: %v", err)
			}
		}
		return nil
	})

	if err != nil {
		return fmt.Errorf("failed to save data to BoltDB: %v", err)
	}

	return nil
}

// ReadFromBoltDB reads data from the specified BoltDB database and bucket.
// dbName is the name of the BoltDB database.
// bucketName is the name of the bucket where the data is stored.
// The function returns a slice of interface{} containing the deserialized data.
func ReadFromBoltDB(dbName, bucketName string) ([]interface{}, error) {
	// Open the BoltDB database
	db, err := bbolt.Open(dbName, 0666, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to open BoltDB: %v", err)
	}
	defer db.Close()

	var data []interface{}

	// Perform the transaction
	err = db.View(func(tx *bbolt.Tx) error {
		// Access the bucket where the data is stored
		bucket := tx.Bucket([]byte(bucketName))
		if bucket == nil {
			return fmt.Errorf("bucket %s not found", bucketName)
		}

		// Iterate through all keys in the bucket
		return bucket.ForEach(func(k, v []byte) error {
			// Unmarshal the data from JSON
			var item interface{}
			if err := json.Unmarshal(v, &item); err != nil {
				return fmt.Errorf("failed to unmarshal item: %v", err)
			}

			// Append the item to the data slice
			data = append(data, item)
			return nil
		})
	})

	if err != nil {
		return nil, fmt.Errorf("failed to read data from BoltDB: %v", err)
	}

	return data, nil
}