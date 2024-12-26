package boltstore

import (
	"encoding/json"
	"errors"
	"fmt"

	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/internal/domain/entities"
)

// NetworkTechnologyBoltDBRepository is the BoltDB implementation of the repository
type NetworkTechnologyBoltDBRepository struct {
	db         *bolt.DB
	bucketName string
}

// NewNetworkTechnologyBoltDBRepository creates a new instance of the BoltDB repository
func NewNetworkTechnologyBoltDBRepository(db *bolt.DB, bucketName string) (*NetworkTechnologyBoltDBRepository, error) {
	// Ensure the bucket is initialized
	err := db.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucketIfNotExists([]byte(bucketName))
		if err != nil {
			return fmt.Errorf("failed to create bucket: %w", err)
		}
		return nil
	})
	if err != nil {
		return nil, err
	}

	return &NetworkTechnologyBoltDBRepository{
		db:         db,
		bucketName: bucketName,
	}, nil
}

// Save saves a NetworkTechnology to BoltDB
func (r *NetworkTechnologyBoltDBRepository) Save(networkTechnology entities.NetworkTechnology) error {
	return r.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte(r.bucketName))
		if bucket == nil {
			return fmt.Errorf("bucket '%s' not found", r.bucketName)
		}

		// Serialize the entity to JSON
		data, err := json.Marshal(networkTechnology)
		if err != nil {
			return fmt.Errorf("failed to serialize network technology: %w", err)
		}

		return bucket.Put([]byte(networkTechnology.ID), data)
	})
}

// FindAll retrieves all NetworkTechnologies from BoltDB
func (r *NetworkTechnologyBoltDBRepository) FindAll() ([]entities.NetworkTechnology, error) {
	var technologies []entities.NetworkTechnology

	err := r.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte(r.bucketName))
		if bucket == nil {
			return fmt.Errorf("bucket '%s' not found", r.bucketName)
		}

		return bucket.ForEach(func(k, v []byte) error {
			var tech entities.NetworkTechnology
			if err := json.Unmarshal(v, &tech); err != nil {
				return fmt.Errorf("failed to deserialize network technology: %w", err)
			}
			technologies = append(technologies, tech)
			return nil
		})
	})
	return technologies, err
}

// FindByID retrieves a NetworkTechnology by its ID from BoltDB
func (r *NetworkTechnologyBoltDBRepository) FindByID(id string) (entities.NetworkTechnology, error) {
	var networkTechnology entities.NetworkTechnology

	err := r.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte(r.bucketName))
		if bucket == nil {
			return fmt.Errorf("bucket '%s' not found", r.bucketName)
		}

		data := bucket.Get([]byte(id))
		if data == nil {
			return errors.New("network technology not found")
		}

		if err := json.Unmarshal(data, &networkTechnology); err != nil {
			return fmt.Errorf("failed to deserialize network technology: %w", err)
		}
		return nil
	})
	return networkTechnology, err
}

// Delete removes a NetworkTechnology by its ID from BoltDB
func (r *NetworkTechnologyBoltDBRepository) Delete(id string) error {
	return r.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte(r.bucketName))
		if bucket == nil {
			return fmt.Errorf("bucket '%s' not found", r.bucketName)
		}

		return bucket.Delete([]byte(id))
	})
}
