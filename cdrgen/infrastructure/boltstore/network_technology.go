package boltstore

import (
	"fmt"
	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkTechnologyRepository extends BoltRepository with specific domain logic for NetworkTechnology.
type NetworkTechnologyRepository struct {
	*BoltRepository // Embedding BoltRepository
}

// NewNetworkTechnologyRepository creates a new instance of NetworkTechnologyRepository.
func NewNetworkTechnologyRepository(dbPath, bucketName string) (*NetworkTechnologyRepository, error) {
	baseRepo, err := NewBoltRepository(dbPath, bucketName)
	if err != nil {
		return nil, fmt.Errorf("error creating repository: %w", err)
	}

	return &NetworkTechnologyRepository{
		BoltRepository: baseRepo,
	}, nil
}

// Create inserts a new NetworkTechnology into the database.
func (r *NetworkTechnologyRepository) Create(tech entities.NetworkTechnology) (entities.NetworkTechnology, error) {
	// Check if a NetworkTechnology with the same name already exists
	existingTech, found, err := r.FindByName(tech.Name)
	if err != nil {
		return entities.NetworkTechnology{}, fmt.Errorf("error checking if technology exists: %w", err)
	}
	if found {
		return entities.NetworkTechnology{}, fmt.Errorf("network technology with name '%s' already exists", existingTech.Name)
	}

	// Insert the new technology
	itemID, err := r.BoltRepository.Create(tech.ID, tech)
	if err != nil {
		return entities.NetworkTechnology{}, fmt.Errorf("error creating network technology: %w", err)
	}
	tech.ID = itemID
	return tech, nil
}

// FindByName retrieves a NetworkTechnology by its name.
func (r *NetworkTechnologyRepository) FindByName(name string) (entities.NetworkTechnology, bool, error) {
	var tech entities.NetworkTechnology
	err := r.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(r.bucketName))
		c := b.Cursor()

		for k, v := c.First(); k != nil; k, v = c.Next() {
			err := r.Deserialize(v, &tech)
			if err != nil {
				return err
			}
			if tech.Name == name {
				return nil
			}
		}
		return fmt.Errorf("network technology not found")
	})

	if err != nil {
		return entities.NetworkTechnology{}, false, err
	}

	return tech, true, nil
}

// FindAll retrieves all NetworkTechnologies from the database.
func (r *NetworkTechnologyRepository) FindAll() ([]entities.NetworkTechnology, error) {
	var technologies []entities.NetworkTechnology

	err := r.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(r.bucketName))

		return b.ForEach(func(k, v []byte) error {
			var tech entities.NetworkTechnology
			if err := r.Deserialize(v, &tech); err == nil {
				technologies = append(technologies, tech)
			}
			return nil
		})
	})

	if err != nil {
		return nil, err
	}

	return technologies, nil
}
