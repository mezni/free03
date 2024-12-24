package boltstore

import (
	"github.com/mezni/wovoka/configurator/domain/entities"
	"github.com/boltdb/bolt"
	"errors"
	"math/rand"
	"time"
)

// BoltDBLocationRepository is a repository that stores locations in a BoltDB database.
type BoltDBLocationRepository struct {
	db *bolt.DB
}

// NewBoltDBLocationRepository creates a new BoltDB-backed location repository.
func NewBoltDBLocationRepository(dbFile string) (*BoltDBLocationRepository, error) {
	db, err := bolt.Open(dbFile, 0600, nil)
	if err != nil {
		return nil, err
	}

	return &BoltDBLocationRepository{db: db}, nil
}

// Create adds a new location to the repository.
func (repo *BoltDBLocationRepository) Create(location *entities.Location) error {
	return repo.db.Update(func(tx *bolt.Tx) error {
		bucket, err := tx.CreateBucketIfNotExists([]byte("locations"))
		if err != nil {
			return err
		}

		// Serialize location and save
		data := serializeLocation(location)
		return bucket.Put(itob(location.LocationID), data)
	})
}

// GetByID retrieves a location by its ID.
func (repo *BoltDBLocationRepository) GetByID(id int) (*entities.Location, error) {
	var location *entities.Location

	err := repo.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return errors.New("bucket not found")
		}

		data := bucket.Get(itob(id))
		if data == nil {
			return errors.New("location not found")
		}

		location = deserializeLocation(data)
		return nil
	})

	if err != nil {
		return nil, err
	}
	return location, nil
}

// Update updates an existing location in the repository.
func (repo *BoltDBLocationRepository) Update(location *entities.Location) error {
	return repo.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return errors.New("bucket not found")
		}

		// Serialize location and update
		data := serializeLocation(location)
		return bucket.Put(itob(location.LocationID), data)
	})
}

// Delete removes a location by its ID.
func (repo *BoltDBLocationRepository) Delete(id int) error {
	return repo.db.Update(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return errors.New("bucket not found")
		}

		return bucket.Delete(itob(id))
	})
}

// GetAll retrieves all locations from the repository.
func (repo *BoltDBLocationRepository) GetAll() ([]*entities.Location, error) {
	var locations []*entities.Location

	err := repo.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return errors.New("bucket not found")
		}

		cursor := bucket.Cursor()
		for k, v := cursor.First(); k != nil; k, v = cursor.Next() {
			location := deserializeLocation(v)
			locations = append(locations, location)
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	return locations, nil
}

// GetRandomByNetworkType retrieves a random location by network type.
func (repo *BoltDBLocationRepository) GetRandomByNetworkType(networkType entities.NetworkType) (*entities.Location, error) {
	var filteredLocations []*entities.Location

	err := repo.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("locations"))
		if bucket == nil {
			return errors.New("bucket not found")
		}

		cursor := bucket.Cursor()
		for k, v := cursor.First(); k != nil; k, v = cursor.Next() {
			location := deserializeLocation(v)
			if location.NetworkType == networkType {
				filteredLocations = append(filteredLocations, location)
			}
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	if len(filteredLocations) == 0 {
		return nil, errors.New("no locations found for the given network type")
	}

	rand.Seed(time.Now().UnixNano())
	randomIndex := rand.Intn(len(filteredLocations))
	return filteredLocations[randomIndex], nil
}

// Helper function to serialize a location
func serializeLocation(location *entities.Location) []byte {
	// Implement the serialization (could be JSON, Gob, etc.)
}

// Helper function to deserialize a location
func deserializeLocation(data []byte) *entities.Location {
	// Implement deserialization (could be JSON, Gob, etc.)
}

// Helper function to convert int to byte slice
func itob(i int) []byte {
	return []byte(string(i))
}
