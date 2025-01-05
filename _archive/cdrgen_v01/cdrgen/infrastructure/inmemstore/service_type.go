package inmemstore

import (
	"errors"
	"sync"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// InMemServiceTypeRepository is an in-memory implementation of ServiceTypeRepository.
type InMemServiceTypeRepository struct {
	data map[int]entities.ServiceType
	mu   sync.RWMutex
}

// NewInMemServiceTypeRepository creates a new in-memory repository instance for service types.
func NewInMemServiceTypeRepository() *InMemServiceTypeRepository {
	return &InMemServiceTypeRepository{
		data: make(map[int]entities.ServiceType),
	}
}

// Insert adds a new ServiceType to the repository.
func (repo *InMemServiceTypeRepository) Insert(serviceType entities.ServiceType) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	if _, exists := repo.data[serviceType.ID]; exists {
		return errors.New("service type with the same ID already exists")
	}

	repo.data[serviceType.ID] = serviceType
	return nil
}

// GetAll retrieves all ServiceType entities from the repository.
func (repo *InMemServiceTypeRepository) GetAll() ([]entities.ServiceType, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	var serviceTypes []entities.ServiceType
	for _, serviceType := range repo.data {
		serviceTypes = append(serviceTypes, serviceType)
	}

	return serviceTypes, nil
}
