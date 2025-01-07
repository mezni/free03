package inmemstore

import (
	"errors"
	"sync"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// InMemNetworkElementRepository is an in-memory implementation of NetworkElementRepository.
type InMemNetworkElementRepository struct {
	data map[int]entities.NetworkElement
	mu   sync.RWMutex
}

// NewInMemNetworkElementRepository creates a new in-memory repository instance for network elements.
func NewInMemNetworkElementRepository() *InMemNetworkElementRepository {
	return &InMemNetworkElementRepository{
		data: make(map[int]entities.NetworkElement),
	}
}

// Insert adds a new NetworkElement to the repository.
func (repo *InMemNetworkElementRepository) Insert(networkElement entities.NetworkElement) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	if _, exists := repo.data[networkElement.ID]; exists {
		return errors.New("network element with the same ID already exists")
	}

	repo.data[networkElement.ID] = networkElement
	return nil
}

// GetAll retrieves all NetworkElement entities from the repository.
func (repo *InMemNetworkElementRepository) GetAll() ([]entities.NetworkElement, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	var elements []entities.NetworkElement
	for _, element := range repo.data {
		elements = append(elements, element)
	}

	return elements, nil
}
