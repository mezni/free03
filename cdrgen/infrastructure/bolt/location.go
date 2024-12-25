package bolt

import (
	"encoding/json"
	"errors"
	"fmt"
	"math/rand"
	"time"

	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// BoltDBLocationRepository is an implementation of the LocationRepository interface for BoltDB.
type BoltDBLocationRepository struct {
	db *bolt.DB
}

// NewBoltDBLocationRepository creates a new instance of BoltDBLocationRepository.
func NewBoltDBLocationRepository(dbName string) (*BoltDBLocationRepository, error) {
	db, err := bolt.Open(dbName, 0600, nil)
	if err != nil {
		return nil, err
	}
	return &BoltDBLocationRepository{db: db}, nil
}

// Create inserts a single location into the BoltDB repository.
func (repo *BoltDBLocationRepository) Create(location *entities.Location) error {
	return repo.db.Update(func(tx *bolt.Tx) error {
		bucket, err := tx.CreateBucketIfNotExists([]byte("Locations"))
		if err != nil {
			return err
		}

		// Serialize the Location into JSON
		data, err := json.Marshal(location)
		if err != nil {
			return err
		}

		// Use the location's ID as the key (corrected conversion)
		err = bucket.Put([]byte(fmt.Sprintf("%d", location.LocationID)), data)
		if err != nil {
			return err
		}

		return nil
	})
}

// CreateMultiple inserts multiple locations into the BoltDB repository.
func (repo *BoltDBLocationRepository) CreateMultiple(locations []*entities.Location) error {
	return repo.db.Update(func(tx *bolt.Tx) error {
		bucket, err := tx.CreateBucketIfNotExists([]byte("Locations"))
		if err != nil {
			return err
		}

		for _, location := range locations {
			// Serialize each Location into JSON
			data, err := json.Marshal(location)
			if err != nil {
				return err
			}

			// Use the location's ID as the key (corrected conversion)
			err = bucket.Put([]byte(fmt.Sprintf("%d", location.LocationID)), data)
			if err != nil {
				return err
			}
		}

		return nil
	})
}

// GetAll retrieves all locations from the BoltDB repository.
func (repo *BoltDBLocationRepository) GetAll() ([]*entities.Location, error) {
	var locations []*entities.Location

	err := repo.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("Locations"))
		if bucket == nil {
			return errors.New("bucket not found")
		}

		cursor := bucket.Cursor()
		for k, v := cursor.First(); k != nil; k, v = cursor.Next() {
			var location entities.Location

			// Deserialize the JSON data into a Location object
			err := json.Unmarshal(v, &location)
			if err != nil {
				return err
			}
			locations = append(locations, &location)
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	return locations, nil
}

// GetRandomByNetworkType returns a random location filtered by network type.
func (repo *BoltDBLocationRepository) GetRandomByNetworkType(networkType entities.NetworkType) (*entities.Location, error) {
	var locations []*entities.Location

	err := repo.db.View(func(tx *bolt.Tx) error {
		bucket := tx.Bucket([]byte("Locations"))
		if bucket == nil {
			return errors.New("bucket not found")
		}

		cursor := bucket.Cursor()
		for k, v := cursor.First(); k != nil; k, v = cursor.Next() {
			var location entities.Location

			// Deserialize the JSON data into a Location object
			err := json.Unmarshal(v, &location)
			if err != nil {
				return err
			}

			// Filter by network type
			if location.NetworkType == networkType {
				locations = append(locations, &location)
			}
		}
		return nil
	})

	if err != nil {
		return nil, err
	}

	if len(locations) == 0 {
		return nil, errors.New("no locations found for the specified network type")
	}

	// Select a random location from the filtered list
	rand.Seed(time.Now().UnixNano())
	randomIndex := rand.Intn(len(locations))
	return locations[randomIndex], nil
}

// Close closes the BoltDB connection.
func (repo *BoltDBLocationRepository) Close() error {
	return repo.db.Close()
}
