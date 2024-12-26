package inmemstore

import (
	"errors"
	"github.com/mezni/wovoka/cdrgen/internal/domain"
	"sync"
)

// NetworkTechnologyInMemoryRepository is an in-memory implementation of NetworkTechnologyRepository
type NetworkTechnologyInMemoryRepository struct {
	mu                 sync.RWMutex
	networkTechnologies map[string]domain.NetworkTechnology
}

// NewNetworkTechnologyInMemoryRepository creates a new in-memory repository instance
func NewNetworkTechnologyInMemoryRepository() *NetworkTechnologyInMemoryRepository {
	return &NetworkTechnologyInMemoryRepository{
		networkTechnologies: make(map[string]domain.NetworkTechnology),
	}
}

// Save saves a NetworkTechnology to the in-memory repository
func (r *NetworkTechnologyInMemoryRepository) Save(networkTechnology domain.NetworkTechnology) error {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.networkTechnologies[networkTechnology.ID] = networkTechnology
	return nil
}

// FindAll retrieves all NetworkTechnologies from the in-memory repository
func (r *NetworkTechnologyInMemoryRepository) FindAll() ([]domain.NetworkTechnology, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	var result []domain.NetworkTechnology
	for _, nt := range r.networkTechnologies {
		result = append(result, nt)
	}
	return result, nil
}

// FindByID retrieves a NetworkTechnology by its ID
func (r *NetworkTechnologyInMemoryRepository) FindByID(id string) (domain.NetworkTechnology, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	networkTechnology, exists := r.networkTechnologies[id]
	if !exists {
		return domain.NetworkTechnology{}, errors.New("NetworkTechnology not found")
	}
	return networkTechnology, nil
}

// Delete removes a NetworkTechnology by its ID
func (r *NetworkTechnologyInMemoryRepository) Delete(id string) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	_, exists := r.networkTechnologies[id]
	if !exists {
		return errors.New("NetworkTechnology not found")
	}
	delete(r.networkTechnologies, id)
	return nil
}
