package inmemstore

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"sync"
)

// InMemoryNetworkTechnologyRepository is an in-memory implementation of NetworkTechnologyRepository.
type InMemoryNetworkTechnologyRepository struct {
	data map[int]*entities.NetworkTechnology
	mu   sync.RWMutex // Mutex to ensure safe concurrent access
}

// NewInMemoryNetworkTechnologyRepository creates a new instance of InMemoryNetworkTechnologyRepository.
func NewInMemoryNetworkTechnologyRepository() *InMemoryNetworkTechnologyRepository {
	return &InMemoryNetworkTechnologyRepository{
		data: make(map[int]*entities.NetworkTechnology),
	}
}

// Save saves a new network technology or updates an existing one.
func (repo *InMemoryNetworkTechnologyRepository) Save(networkTechnology *entities.NetworkTechnology) error {
	if networkTechnology == nil {
		return fmt.Errorf("network technology cannot be nil")
	}

	// Lock for writing to ensure no other goroutine can modify the data simultaneously
	repo.mu.Lock()
	defer repo.mu.Unlock()

	repo.data[networkTechnology.ID] = networkTechnology
	return nil
}

// FindByID finds a network technology by its ID.
func (repo *InMemoryNetworkTechnologyRepository) FindByID(id int) (*entities.NetworkTechnology, error) {
	// Lock for reading to allow multiple reads but no writes during read
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	networkTechnology, exists := repo.data[id]
	if !exists {
		return nil, fmt.Errorf("network technology with ID %d not found", id)
	}
	return networkTechnology, nil
}

// FindAll retrieves all network technologies.
func (repo *InMemoryNetworkTechnologyRepository) FindAll() ([]*entities.NetworkTechnology, error) {
	// Lock for reading to allow multiple reads but no writes during read
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	var result []*entities.NetworkTechnology
	for _, nt := range repo.data {
		result = append(result, nt)
	}
	return result, nil
}
