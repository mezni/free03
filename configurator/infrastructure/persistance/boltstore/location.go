package boltstore

import (
	"encoding/json"
	"fmt"
	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/configurator/domain/entities"
)

// BoltDBLocationRepository implements the LocationRepository interface using BoltDB.
type BoltDBLocationRepository struct {
	db *bolt.DB
}

// NewBoltDBLocationRepository creates a new BoltDB repository with the provided dbFile path.
func NewBoltDBLocationRepository(dbFile string) (*BoltDBLocationRepository, error) {
	db, err := bolt.Open(dbFile, 0600, nil)
	if err != nil {
		return nil, err
	}

	// Initialize the "locations" bucket if it doesn't exist.
	err = db.Update(func(tx *bolt.Tx) error {
		_, err := tx.CreateBucketIfNotExists([]byte("locations"))
		return err
	})
	if err != nil {
		return nil, err
	}

	return &BoltDBLocationRepository{db: db}, nil
}

// Create a new location in the repository.
func (repo *BoltDBLocationRepository) Create(location *entities.Location) error {
	return repo.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return fmt.Errorf("bucket 'locations' does not exist")
		}

		data, err := json.Marshal(location)
		if err != nil {
			return err
		}

		return bucket.Put([]byte(fmt.Sprintf("%d", location.LocationID)), data)
	})
}

// Get a location by its ID.
func (repo *BoltDBLocationRepository) GetByID(id int) (*entities.Location, error) {
	var location *entities.Location
	err := repo.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return fmt.Errorf("bucket 'locations' does not exist")
		}

		data := bucket.Get([]byte(fmt.Sprintf("%d", id)))
		if data == nil {
			return fmt.Errorf("location not found")
		}

		return json.Unmarshal(data, &location)
	})
	return location, err
}

// Update an existing location in the repository.
func (repo *BoltDBLocationRepository) Update(location *entities.Location) error {
	return repo.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return fmt.Errorf("bucket 'locations' does not exist")
		}

		data, err := json.Marshal(location)
		if err != nil {
			return err
		}

		return bucket.Put([]byte(fmt.Sprintf("%d", location.LocationID)), data)
	})
}

// Delete a location by its ID.
func (repo *BoltDBLocationRepository) Delete(id int) error {
	return repo.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return fmt.Errorf("bucket 'locations' does not exist")
		}

		return bucket.Delete([]byte(fmt.Sprintf("%d", id)))
	})
}

// Get all locations from the repository.
func (repo *BoltDBLocationRepository) GetAll() ([]*entities.Location, error) {
	var locations []*entities.Location
	err := repo.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return fmt.Errorf("bucket 'locations' does not exist")
		}

		return bucket.ForEach(func(k, v []byte) error {
			var location *entities.Location
			err := json.Unmarshal(v, &location)
			if err != nil {
				return err
			}
			locations = append(locations, location)
			return nil
		})
	})
	return locations, err
}

// Close the BoltDB connection.
func (repo *BoltDBLocationRepository) Close() error {
	return repo.db.Close()
}
