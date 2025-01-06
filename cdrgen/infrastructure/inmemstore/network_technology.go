package inmemstore

import (
	"errors"
	"sync"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// MemoryNetworkTechnologyRepository is an in-memory implementation of NetworkTechnologyRepository.
type InMemNetworkTechnologyRepository struct {
	data map[int]entities.NetworkTechnology
	mu   sync.RWMutex
}

// NewMemoryNetworkTechnologyRepository creates a new in-memory repository instance.
func NewInMemNetworkTechnologyRepository() *InMemNetworkTechnologyRepository {
	return &InMemNetworkTechnologyRepository{
		data: make(map[int]entities.NetworkTechnology),
	}
}

// Insert adds a new NetworkTechnology to the repository.
func (repo *InMemNetworkTechnologyRepository) Insert(networkTechnology entities.NetworkTechnology) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	if _, exists := repo.data[networkTechnology.ID]; exists {
		return errors.New("network technology with the same ID already exists")
	}

	repo.data[networkTechnology.ID] = networkTechnology
	return nil
}

// GetAll retrieves all NetworkTechnology entities from the repository.
func (repo *InMemNetworkTechnologyRepository) GetAll() ([]entities.NetworkTechnology, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	var technologies []entities.NetworkTechnology
	for _, tech := range repo.data {
		technologies = append(technologies, tech)
	}

	return technologies, nil
}
