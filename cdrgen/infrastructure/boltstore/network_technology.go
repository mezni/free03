package boltstore

import (
	"fmt"
	"github.com/boltdb/bolt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkTechnologyRepository extends BoltRepository with specific domain logic for NetworkTechnology.
type NetworkTechnologyRepository struct {
	*BoltRepository // Embedding BoltRepository to reuse methods
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

// Create inserts a new NetworkTechnology into the database, or returns the existing one if a technology with the same name exists.
func (r *NetworkTechnologyRepository) Create(tech entities.NetworkTechnology) (entities.NetworkTechnology, error) {
	// Check if a NetworkTechnology with the same name already exists
	existingTech, found, err := r.FindByName(tech.Name)
	if err != nil {
		return entities.NetworkTechnology{}, fmt.Errorf("failed to check if technology exists: %w", err)
	}
	if found {
		// If technology exists, return the existing one and no error
		return existingTech, nil
	}

	// Insert the new technology
	itemID, err := r.BoltRepository.Create(tech.ID, tech)
	if err != nil {
		return entities.NetworkTechnology{}, fmt.Errorf("failed to create network technology: %w", err)
	}
	tech.ID = itemID
	return tech, nil
}

// FindByName retrieves a NetworkTechnology by its name.
func (r *NetworkTechnologyRepository) FindByName(name string) (entities.NetworkTechnology, bool, error) {
	var tech entities.NetworkTechnology
	found := false
	err := r.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(r.bucketName))
		c := b.Cursor()

		// Iterate through the entries in the bucket
		for k, v := c.First(); k != nil; k, v = c.Next() {
			err := r.Deserialize(v, &tech)
			if err != nil {
				// Ignore the error if deserialization fails
				continue
			}
			if tech.Name == name {
				found = true
				return nil
			}
		}
		return nil
	})

	if err != nil {
		return entities.NetworkTechnology{}, false, err
	}

	if found {
		return tech, true, nil
	}
	return entities.NetworkTechnology{}, false, nil
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

// CreateMany inserts a slice of NetworkTechnologies into the database.
func (r *NetworkTechnologyRepository) CreateMany(technologies []entities.NetworkTechnology) ([]entities.NetworkTechnology, error) {
	var createdTechnologies []entities.NetworkTechnology
	for _, tech := range technologies {
		existingTech, found, err := r.FindByName(tech.Name)
		if err != nil {
			return nil, fmt.Errorf("error checking if technology exists: %w", err)
		}

		if found {
			createdTechnologies = append(createdTechnologies, existingTech)
			continue
		}

		itemID, err := r.BoltRepository.Create(tech.ID, tech)
		if err != nil {
			return nil, fmt.Errorf("failed to create network technology: %w", err)
		}
		tech.ID = itemID
		createdTechnologies = append(createdTechnologies, tech)
	}
	return createdTechnologies, nil
}

// GetMaxID retrieves the maximum ID assigned to NetworkTechnologies in the database.
func (r *NetworkTechnologyRepository) GetMaxID() (int, error) {
	var maxID int
	err := r.db.View(func(tx *bolt.Tx) error {
		b := tx.Bucket([]byte(r.bucketName))
		c := b.Cursor()

		for k, v := c.First(); k != nil; k, v = c.Next() {
			var tech entities.NetworkTechnology
			if err := r.Deserialize(v, &tech); err == nil {
				if tech.ID > maxID {
					maxID = tech.ID
				}
			}
		}
		return nil
	})

	if err != nil {
		return 0, err
	}
	return maxID, nil
}
