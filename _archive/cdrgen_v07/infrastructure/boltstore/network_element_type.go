package boltstore

import (
	"fmt"
	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkElementTypeRepository extends BoltRepository with specific domain logic for NetworkElementType.
type NetworkElementTypeRepository struct {
	*BoltRepository // Embedding BoltRepository to reuse methods
}

// NewNetworkElementTypeRepository creates a new instance of NetworkElementTypeRepository.
func NewNetworkElementTypeRepository(dbPath, bucketName string) (*NetworkElementTypeRepository, error) {
	baseRepo, err := NewBoltRepository(dbPath, bucketName)
	if err != nil {
		return nil, fmt.Errorf("error creating repository: %w", err)
	}

	return &NetworkElementTypeRepository{
		BoltRepository: baseRepo,
	}, nil
}

// Create inserts a new NetworkElementType into the database, or returns the existing one if a technology with the same name exists.
func (r *NetworkElementTypeRepository) Create(netElemType entities.NetworkElementType) (entities.NetworkElementType, error) {
	// Check if a NetworkElementType with the same name already exists
	existingElem, found, err := r.FindByName(netElemType.Name)
	if err != nil {
		return entities.NetworkElementType{}, fmt.Errorf("failed to check if element type exists: %w", err)
	}
	if found {
		// If element type exists, return the existing one and no error
		return existingElem, nil
	}

	// Insert the new element type
	itemID, err := r.BoltRepository.Create(netElemType.ID, netElemType)
	if err != nil {
		return entities.NetworkElementType{}, fmt.Errorf("failed to create network element type: %w", err)
	}
	netElemType.ID = itemID

	return netElemType, nil
}

// FindByName retrieves a NetworkElementType by its name.
func (r *NetworkElementTypeRepository) FindByName(name string) (entities.NetworkElementType, bool, error) {
	var netElemType entities.NetworkElementType
	found := false
	err := r.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(r.bucketName))
		c := b.Cursor()

		// Iterate through the entries in the bucket
		for k, v := c.First(); k != nil; k, v = c.Next() {
			err := r.Deserialize(v, &netElemType) // Deserialization error handling
			if err != nil {
				// Ignore the error if deserialization fails (we can handle invalid data later)
				continue
			}
			// If the name matches, set found to true and return the element type
			if netElemType.Name == name {
				found = true
				return nil
			}
		}
		return nil
	})

	// Handle the error from the View transaction block
	if err != nil {
		return entities.NetworkElementType{}, false, err
	}

	// If the name is found, return the element type and true
	if found {
		return netElemType, true, nil
	}
	// If the name is not found, return false
	return entities.NetworkElementType{}, false, nil
}

// FindAll retrieves all NetworkElementTypes from the database.
func (r *NetworkElementTypeRepository) FindAll() ([]entities.NetworkElementType, error) {
	var elementTypes []entities.NetworkElementType

	// Start a read-only view transaction on the database
	err := r.db.View(func(tx *bolt.Tx) error {
		// Access the specific bucket within the database
		b := tx.Bucket([]byte(r.bucketName))
		if b == nil {
			return fmt.Errorf("bucket %s not found", r.bucketName)
		}

		// Iterate through all the elements in the bucket
		return b.ForEach(func(k, v []byte) error {
			var netElemType entities.NetworkElementType
			// Deserialize the value into the NetworkElementType struct
			if err := r.Deserialize(v, &netElemType); err == nil {
				// If deserialization is successful, append the element type to the slice
				elementTypes = append(elementTypes, netElemType)
			}
			return nil
		})
	})

	if err != nil {
		return nil, err
	}

	return elementTypes, nil
}
