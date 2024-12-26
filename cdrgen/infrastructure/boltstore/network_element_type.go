package boltdb

import (
    "log"

    "github.com/mezni/wovoka/cdrgen/domain/entities"
)

const networkElementBucketName = "NetworkElementTypes"

// BoltDBNetworkElementTypeRepository implements the NetworkElementTypeRepository interface using BoltDB.
type BoltDBNetworkElementTypeRepository struct {
    BaseRepository
}

// NewBoltDBNetworkElementTypeRepository initializes a new repository for NetworkElementType.
func NewBoltDBNetworkElementTypeRepository(dbPath string) (*BoltDBNetworkElementTypeRepository, error) {
    baseRepo, err := NewBaseRepository(dbPath, networkElementBucketName)
    if err != nil {
        return nil, err
    }

    return &BoltDBNetworkElementTypeRepository{*baseRepo}, nil
}

// Create inserts a single NetworkElementType into the database.
func (r *BoltDBNetworkElementTypeRepository) Create(element entities.NetworkElementType) (entities.NetworkElementType, bool) {
    // Check for existing element by name
    _, exists := r.FindByName(element.Name)
    if exists {
        log.Printf("NetworkElementType with name %s already exists, skipping insert.", element.Name)
        return element, false
    }

    id, err := r.Create(element.ID, element)
    if err != nil {
        log.Printf("Error creating NetworkElementType: %v", err)
        return element, false
    }

    element.ID = id
    return element, true
}

// CreateFromMapSlice creates multiple NetworkElementTypes from a slice of maps.
func (r *BoltDBNetworkElementTypeRepository) CreateFromMapSlice(elementData []map[string]interface{}) ([]entities.NetworkElementType, error) {
    var elements []entities.NetworkElementType

    createFunc := func(itemData map[string]interface{}) (interface{}, error) {
        element := entities.NetworkElementType{
            Name:                  itemData["Name"].(string),
            Description:           itemData["Description"].(string),
            NetworkTechnologyName: itemData["NetworkTechnologyName"].(string),
        }

        createdElement, created := r.Create(element)
        if created {
            return createdElement, nil
        }
        return nil, nil // Not created, return nil
    }

    createdItems, err := r.CreateFromMapSlice(elementData, createFunc)
    if err != nil {
        return nil, err
    }

    for _, item := range createdItems {
        if element, ok := item.(entities.NetworkElementType); ok {
            elements = append(elements, element)
        }
    }

    return elements, nil
}

// FindByName retrieves a NetworkElementType by its name.
func (r *BoltDBNetworkElementTypeRepository) FindByName(name string) (entities.NetworkElementType, bool) {
    var element entities.NetworkElementType
    found := false

    err := r.db.View(func(tx *bolt.Tx) error {
        b := tx.Bucket([]byte(networkElementBucketName))

        return b.ForEach(func(k, v []byte) error {
            netElement := entities.NetworkElementType{} // Initialize your struct here
            if err := r.Deserialize(v, &netElement); err == nil {
                if netElement.Name == name {
                    element = netElement
                    found = true
                    return nil // Stop iteration
                }
            }
            return nil
        })
    })

    if err != nil {
        log.Printf("Error finding NetworkElementType by name: %v", err)
    }

    return element, found
}

// FindAll retrieves all NetworkElementTypes from the database.
func (r *BoltDBNetworkElementTypeRepository) FindAll() []entities.NetworkElementType {
    var elements []entities.NetworkElementType
    r.FindAll(&elements)
    return elements
}