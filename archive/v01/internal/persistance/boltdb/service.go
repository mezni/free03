package persistence

import (
	"encoding/json"
	"fmt"
	"github.com/mezni/wovoka/domain/entities"
	"github.com/mezni/wovoka/domain/interfaces"
	"go.etcd.io/bbolt"
)

// BoltServiceRepository implements the ServiceRepository interface using BoltDB as the storage backend.
type BoltServiceRepository struct {
	db *bbolt.DB
}

// NewBoltServiceRepository creates a new instance of BoltServiceRepository.
func NewBoltServiceRepository(dbPath string) (*BoltServiceRepository, error) {
	// Open the BoltDB database file
	db, err := bbolt.Open(dbPath, 0666, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to open BoltDB: %v", err)
	}

	repo := &BoltServiceRepository{db: db}

	// Initialize the bucket if it does not exist
	err = db.Update(func(tx *bbolt.Tx) error {
		_, err := tx.CreateBucketIfNotExists([]byte("Services"))
		return err
	})
	if err != nil {
		return nil, fmt.Errorf("failed to initialize bucket: %v", err)
	}

	return repo, nil
}

// Create stores a new service in the BoltDB repository.
func (repo *BoltServiceRepository) Create(service *entities.Service) error {
	return repo.db.Update(func(tx *bbolt.Tx) error {
		bucket := tx.Bucket([]byte("Services"))
		if bucket == nil {
			return fmt.Errorf("bucket not found")
		}

		// Marshal the service object into JSON format
		data, err := json.Marshal(service)
		if err != nil {
			return fmt.Errorf("failed to marshal service: %v", err)
		}

		// Use the service ID as the key
		return bucket.Put([]byte(fmt.Sprintf("%d", service.ID)), data)
	})
}

// GetByID retrieves a service by ID from the BoltDB repository.
func (repo *BoltServiceRepository) GetByID(id int) (*entities.Service, error) {
	var service entities.Service
	err := repo.db.View(func(tx *bbolt.Tx) error {
		bucket := tx.Bucket([]byte("Services"))
		if bucket == nil {
			return fmt.Errorf("bucket not found")
		}

		data := bucket.Get([]byte(fmt.Sprintf("%d", id)))
		if data == nil {
			return fmt.Errorf("service not found")
		}

		// Unmarshal the service data
		return json.Unmarshal(data, &service)
	})
	if err != nil {
		return nil, err
	}
	return &service, nil
}

// GetByName retrieves a service by Name from the BoltDB repository.
func (repo *BoltServiceRepository) GetByName(name string) (*entities.Service, error) {
	var service entities.Service
	err := repo.db.View(func(tx *bbolt.Tx) error {
		bucket := tx.Bucket([]byte("Services"))
		if bucket == nil {
			return fmt.Errorf("bucket not found")
		}

		// Iterate through the bucket and match the name
		return bucket.ForEach(func(k, v []byte) error {
			if err := json.Unmarshal(v, &service); err != nil {
				return err
			}
			if service.Name == name {
				return nil // Found the service
			}
			return nil // Continue iteration
		})
	})
	if err != nil {
		return nil, err
	}
	return &service, nil
}

// Update modifies an existing service in the BoltDB repository.
func (repo *BoltServiceRepository) Update(service *entities.Service) error {
	return repo.db.Update(func(tx *bbolt.Tx) error {
		bucket := tx.Bucket([]byte("Services"))
		if bucket == nil {
			return fmt.Errorf("bucket not found")
		}

		// Marshal the service object into JSON format
		data, err := json.Marshal(service)
		if err != nil {
			return fmt.Errorf("failed to marshal service: %v", err)
		}

		// Use the service ID as the key
		return bucket.Put([]byte(fmt.Sprintf("%d", service.ID)), data)
	})
}

// Delete removes a service by ID from the BoltDB repository.
func (repo *BoltServiceRepository) Delete(id int) error {
	return repo.db.Update(func(tx *bbolt.Tx) error {
		bucket := tx.Bucket([]byte("Services"))
		if bucket == nil {
			return fmt.Errorf("bucket not found")
		}

		// Delete the service using the ID as the key
		return bucket.Delete([]byte(fmt.Sprintf("%d", id)))
	})
}

// List retrieves all services from the BoltDB repository.
func (repo *BoltServiceRepository) List() ([]*entities.Service, error) {
	var services []*entities.Service
	err := repo.db.View(func(tx *bbolt.Tx) error {
		bucket := tx.Bucket([]byte("Services"))
		if bucket == nil {
			return fmt.Errorf("bucket not found")
		}

		// Iterate through the bucket and unmarshal each service
		return bucket.ForEach(func(k, v []byte) error {
			var service entities.Service
			if err := json.Unmarshal(v, &service); err != nil {
				return err
			}
			services = append(services, &service)
			return nil
		})
	})
	if err != nil {
		return nil, err
	}
	return services, nil
}

// Close closes the BoltDB database.
func (repo *BoltServiceRepository) Close() error {
	return repo.db.Close()
}
