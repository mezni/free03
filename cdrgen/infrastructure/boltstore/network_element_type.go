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

// Create inserts a new NetworkElementType into the database.
func (r *NetworkElementTypeRepository) Create(element entities.NetworkElementType) (entities.NetworkElementType, error) {
	// Check if a NetworkElementType with the same name already exists
	existingElement, found, err := r.FindByName(element.Name)
	if err != nil {
		return entities.NetworkElementType{}, fmt.Errorf("error checking if network element type exists: %w", err)
	}
	if found {
		return entities.NetworkElementType{}, fmt.Errorf("network element type with name '%s' already exists", existingElement.Name)
	}

	// Insert the new NetworkElementType
	itemID, err := r.BoltRepository.Create(element.ID, element)
	if err != nil {
		return entities.NetworkElementType{}, fmt.Errorf("error creating network element type: %w", err)
	}
	element.ID = itemID
	return element, nil
}

// FindByName retrieves a NetworkElementType by its name.
func (r *NetworkElementTypeRepository) FindByName(name string) (entities.NetworkElementType, bool, error) {
	var element entities.NetworkElementType
	err := r.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(r.bucketName))
		c := b.Cursor()

		for k, v := c.First(); k != nil; k, v = c.Next() {
			err := r.Deserialize(v, &element)
			if err != nil {
				return err
			}
			if element.Name == name {
				return nil
			}
		}
		return fmt.Errorf("network element type not found")
	})

	if err != nil {
		return entities.NetworkElementType{}, false, err
	}

	return element, true, nil
}

// FindAll retrieves all NetworkElementTypes from the database.
func (r *NetworkElementTypeRepository) FindAll() ([]entities.NetworkElementType, error) {
	var elements []entities.NetworkElementType

	err := r.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(r.bucketName))

		return b.ForEach(func(k, v []byte) error {
			var element entities.NetworkElementType
			if err := r.Deserialize(v, &element); err == nil {
				elements = append(elements, element)
			}
			return nil
		})
	})

	if err != nil {
		return nil, err
	}

	return elements, nil
}
