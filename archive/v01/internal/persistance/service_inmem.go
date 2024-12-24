package persistance

import (
	"errors"
	"sync"

	"github.com/mezni/wovoka/domain/entities"
)

// InMemoryServiceRepository is an in-memory implementation of ServiceRepository.
type InMemoryServiceRepository struct {
	data map[int]*entities.Service
	mu   sync.RWMutex
}

// NewInMemoryServiceRepository creates a new instance of the in-memory repository.
func NewInMemoryServiceRepository() *InMemoryServiceRepository {
	return &InMemoryServiceRepository{
		data: make(map[int]*entities.Service),
	}
}

// Create adds a new service to the repository.
func (repo *InMemoryServiceRepository) Create(service *entities.Service) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	if _, exists := repo.data[service.ID]; exists {
		return errors.New("service with this ID already exists")
	}
	repo.data[service.ID] = service
	return nil
}

// GetByID retrieves a service by ID.
func (repo *InMemoryServiceRepository) GetByID(id int) (*entities.Service, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	service, exists := repo.data[id]
	if !exists {
		return nil, errors.New("service not found")
	}
	return service, nil
}

// GetByName retrieves a service by Name.
func (repo *InMemoryServiceRepository) GetByName(name string) (*entities.Service, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	for _, service := range repo.data {
		if service.Name == name {
			return service, nil
		}
	}
	return nil, errors.New("service not found")
}

// Update modifies an existing service.
func (repo *InMemoryServiceRepository) Update(service *entities.Service) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	if _, exists := repo.data[service.ID]; !exists {
		return errors.New("service not found")
	}
	repo.data[service.ID] = service
	return nil
}

// Delete removes a service by ID.
func (repo *InMemoryServiceRepository) Delete(id int) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	if _, exists := repo.data[id]; !exists {
		return errors.New("service not found")
	}
	delete(repo.data, id)
	return nil
}

// List retrieves all services.
func (repo *InMemoryServiceRepository) List() ([]*entities.Service, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	var services []*entities.Service
	for _, service := range repo.data {
		services = append(services, service)
	}
	return services, nil
}
