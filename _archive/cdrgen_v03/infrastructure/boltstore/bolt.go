package boltstore

import (
	"encoding/json"
	"errors"
	"github.com/boltdb/bolt"
)

type ConfigRepository struct {
	manager *BoltDBManager
}

// NewConfigRepository initializes the repository
func NewConfigRepository(manager *BoltDBManager) *ConfigRepository {
	return &ConfigRepository{
		manager: manager,
	}
}

// Save stores a key-value pair in the specified bucket
func (repo *ConfigRepository) Save(bucketName, key string, value interface{}) error {
	return repo.manager.WithTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		data, err := json.Marshal(value)
		if err != nil {
			return err
		}
		return bucket.Put([]byte(key), data)
	})
}

// SaveMany stores multiple key-value pairs in the specified bucket
func (repo *ConfigRepository) SaveMany(bucketName string, items map[string]interface{}) error {
	return repo.manager.WithTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		for key, value := range items {
			data, err := json.Marshal(value)
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

// Get retrieves a value by key from the specified bucket
func (repo *ConfigRepository) Get(bucketName, key string, value interface{}) error {
	return repo.manager.WithReadOnlyTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		data := bucket.Get([]byte(key))
		if data == nil {
			return errors.New("key not found")
		}
		return json.Unmarshal(data, value)
	})
}

// GetAll retrieves all key-value pairs from the specified bucket
func (repo *ConfigRepository) GetAll(bucketName string, values interface{}) error {
	return repo.manager.WithReadOnlyTransaction(bucketName, func(tx *bolt.Tx, bucket *bolt.Bucket) error {
		var items []json.RawMessage

		err := bucket.ForEach(func(_, v []byte) error {
			items = append(items, v)
			return nil
		})
		if err != nil {
			return err
		}

		data, err := json.Marshal(items)
		if err != nil {
			return err
		}

		return json.Unmarshal(data, values)
	})
}
