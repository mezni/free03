package boltdb

import (
    "log"

    "github.com/mezni/wovoka/cdrgen/domain/entities"
)

const networkTechnologyBucketName = "NetworkTechnologies"

// BoltDBNetworkTechnologyRepository implements the NetworkTechnologyRepository interface using BoltDB.
type BoltDBNetworkTechnologyRepository struct {
    BaseRepository
}

// NewBoltDBNetworkTechnologyRepository initializes a new NetworkTechnology repository.
func NewBoltDBNetworkTechnologyRepository(dbPath string) (*BoltDBNetworkTechnologyRepository, error) {
    baseRepo, err := NewBaseRepository(dbPath, networkTechnologyBucketName)
    if err != nil {
        return nil, err
    }

    return &BoltDBNetworkTechnologyRepository{*baseRepo}, nil
}

// Create inserts a single NetworkTechnology into the database.
func (r *BoltDBNetworkTechnologyRepository) Create(tech entities.NetworkTechnology) (entities.NetworkTechnology, bool) {
    // Check for existing technology by name
    _, exists := r.FindByName(tech.Name)
    if exists {
        log.Printf("NetworkTechnology with name %s already exists, skipping insert.", tech.Name)
        return tech, false
    }

    id, err := r.Create(tech.ID, tech)
    if err != nil {
        log.Printf("Error creating NetworkTechnology: %v", err)
        return tech, false
    }

    tech.ID = id
    return tech, true
}

// CreateFromMapSlice creates multiple NetworkTechnologies from a slice of maps.
func (r *BoltDBNetworkTechnologyRepository) CreateFromMapSlice(elementData []map[string]interface{}) ([]entities.NetworkTechnology, error) {
    var technologies []entities.NetworkTechnology

    createFunc := func(itemData map[string]interface{}) (interface{}, error) {
        tech := entities.NetworkTechnology{
            Name:        itemData["Name"].(string),
            Description: itemData["Description"].(string),
        }

        createdTech, created := r.Create(tech)
        if created {
            return createdTech, nil
        }
        return nil, nil // Not created, return nil
    }

    createdItems, err := r.CreateFromMapSlice(elementData, createFunc)
    if err != nil {
        return nil, err
    }

    for _, item := range createdItems {
        if tech, ok := item.(entities.NetworkTechnology); ok {
            technologies = append(technologies, tech)
        }
    }

    return technologies, nil
}

// FindByName retrieves a NetworkTechnology by its name.
func (r *BoltDBNetworkTechnologyRepository) FindByName(name string) (entities.NetworkTechnology, bool) {
    var tech entities.NetworkTechnology
    found := false

    err := r.db.View(func(tx *bolt.Tx) error {
        b := tx.Bucket([]byte(networkTechnologyBucketName))

        return b.ForEach(func(k, v []byte) error {
            nt := entities.NetworkTechnology{} // Initialize your struct here
            if err := r.Deserialize(v, &nt); err == nil {
                if nt.Name == name {
                    tech = nt
                    found = true
                    return nil // Stop iteration
                }
            }
            return nil
        })
    })

    if err != nil {
        log.Printf("Error finding NetworkTechnology by name: %v", err)
    }

    return tech, found
}

// FindAll retrieves all NetworkTechnologies from the database.
func (r *BoltDBNetworkTechnologyRepository) FindAll() []entities.NetworkTechnology {
    var technologies []entities.NetworkTechnology
    r.FindAll(&technologies)
    return technologies
}