package inmemstore

import (
	"errors"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"math/rand"
	"strings"
	"sync"
	"time"
)

// InMemServiceTypeRepository is an in-memory implementation of ServiceTypeRepository.
type InMemServiceTypeRepository struct {
	data map[int]entities.ServiceType
	mu   sync.RWMutex
}

// NewInMemServiceTypeRepository creates a new in-memory repository instance for service types.
func NewInMemServiceTypeRepository() *InMemServiceTypeRepository {
	// Initialize the random seed
	rand.Seed(time.Now().UnixNano())
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

// GetByNetworkTechnologyAndName retrieves a ServiceType where NetworkTechnology matches exactly,
// and Name contains the given name in a case-insensitive manner. If no such match is found,
// it returns a random ServiceType with the same NetworkTechnology.
func (repo *InMemServiceTypeRepository) GetByNetworkTechnologyAndName(networkTechnology, name string) (entities.ServiceType, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	upperName := strings.ToUpper(name)
	var fallbackCandidates []entities.ServiceType

	for _, serviceType := range repo.data {
		// Check if NetworkTechnology matches exactly
		if serviceType.NetworkTechnology == networkTechnology {
			// Add to fallback candidates
			fallbackCandidates = append(fallbackCandidates, serviceType)

			// Check if Name contains the input name (case-insensitive)
			if strings.Contains(strings.ToUpper(serviceType.Name), upperName) {
				return serviceType, nil
			}
		}
	}

	// If no exact match, return a random fallback candidate
	if len(fallbackCandidates) > 0 {
		randomIndex := rand.Intn(len(fallbackCandidates))
		return fallbackCandidates[randomIndex], nil
	}

	return entities.ServiceType{}, errors.New("no service type found for the given network technology and name")
}
