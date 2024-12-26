package boltstore

import (
	"errors"
	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/internal/domain/entities"
)

// NetworkTechnologyBoltDBRepository is the BoltDB implementation of the repository
type NetworkTechnologyBoltDBRepository struct {
	db *bolt.DB
}

// NewNetworkTechnologyBoltDBRepository creates a new instance of the BoltDB repository
func NewNetworkTechnologyBoltDBRepository(db *bolt.DB) *NetworkTechnologyBoltDBRepository {
	return &NetworkTechnologyBoltDBRepository{
		db: db,
	}
}

// Save saves a NetworkTechnology to BoltDB
func (r *NetworkTechnologyBoltDBRepository) Save(networkTechnology entities.NetworkTechnology) error {
	return r.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("NetworkTechnologies"))
		if bucket == nil {
			return errors.New("NetworkTechnologies bucket not found")
		}
		return bucket.Put([]byte(networkTechnology.ID), []byte(networkTechnology.Name))
	})
}

// FindAll retrieves all NetworkTechnologies from BoltDB
func (r *NetworkTechnologyBoltDBRepository) FindAll() ([]entities.NetworkTechnology, error) {
	var technologies []entities.NetworkTechnology
	err := r.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("NetworkTechnologies"))
		if bucket == nil {
			return errors.New("NetworkTechnologies bucket not found")
		}

		return bucket.ForEach(func(k, v []byte) error {
			technologies = append(technologies, entities.NetworkTechnology{
				ID:   string(k),
				Name: string(v),
			})
			return nil
		})
	})
	return technologies, err
}

// FindByID retrieves a NetworkTechnology by its ID from BoltDB
func (r *NetworkTechnologyBoltDBRepository) FindByID(id string) (entities.NetworkTechnology, error) {
	var networkTechnology entities.NetworkTechnology
	err := r.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("NetworkTechnologies"))
		if bucket == nil {
			return errors.New("NetworkTechnologies bucket not found")
		}
		data := bucket.Get([]byte(id))
		if data == nil {
			return errors.New("NetworkTechnology not found")
		}
		networkTechnology = entities.NetworkTechnology{
			ID:   id,
			Name: string(data),
		}
		return nil
	})
	return networkTechnology, err
}

// Delete removes a NetworkTechnology by its ID from BoltDB
func (r *NetworkTechnologyBoltDBRepository) Delete(id string) error {
	return r.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("NetworkTechnologies"))
		if bucket == nil {
			return errors.New("NetworkTechnologies bucket not found")
		}
		return bucket.Delete([]byte(id))
	})
}
