package inmemstore

import (
	"errors"
	"sync"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkTechnologyRepositoryInMemory is an in-memory implementation of the NetworkTechnologyRepository.
type NetworkTechnologyRepositoryInMemory struct {
	mu                  sync.RWMutex
	networkTechnologies map[int]*entities.NetworkTechnology
}

// NewNetworkTechnologyRepositoryInMemory creates a new instance of NetworkTechnologyRepositoryInMemory.
func NewNetworkTechnologyRepositoryInMemory() *NetworkTechnologyRepositoryInMemory {
	return &NetworkTechnologyRepositoryInMemory{
		networkTechnologies: make(map[int]*entities.NetworkTechnology),
	}
}

// Save saves a new network technology or updates an existing one.
func (r *NetworkTechnologyRepositoryInMemory) Save(networkTechnology *entities.NetworkTechnology) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if networkTechnology == nil {
		return errors.New("network technology cannot be nil")
	}

	r.networkTechnologies[networkTechnology.ID] = networkTechnology
	return nil
}

// FindAll retrieves all network technologies.
func (r *NetworkTechnologyRepositoryInMemory) FindAll() ([]*entities.NetworkTechnology, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	var result []*entities.NetworkTechnology
	for _, tech := range r.networkTechnologies {
		result = append(result, tech)
	}
	return result, nil
}
