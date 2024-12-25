package inmem

import (
	"errors"
	"fmt"
	"math/rand"
	"sync"
	"time"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// InMemoryLocationRepository is an in-memory implementation of the LocationRepository.
type InMemoryLocationRepository struct {
	locations map[int]*entities.Location
	mu        sync.RWMutex // Lock to synchronize access
}

// NewInMemoryLocationRepository creates a new instance of InMemoryLocationRepository.
func NewInMemoryLocationRepository() *InMemoryLocationRepository {
	return &InMemoryLocationRepository{
		locations: make(map[int]*entities.Location),
	}
}

// Create inserts a location into the repository.
func (repo *InMemoryLocationRepository) Create(location *entities.Location) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	if _, exists := repo.locations[location.LocationID]; exists {
		return errors.New("location with this ID already exists")
	}
	repo.locations[location.LocationID] = location
	return nil
}

// CreateMultiple inserts multiple locations into the repository.
func (repo *InMemoryLocationRepository) CreateMultiple(locations []*entities.Location) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	var errors []error
	for _, location := range locations {
		if _, exists := repo.locations[location.LocationID]; exists {
			errors = append(errors, fmt.Errorf("location ID %d already exists", location.LocationID))
			continue
		}
		repo.locations[location.LocationID] = location
	}

	if len(errors) > 0 {
		return fmt.Errorf("failed to insert one or more locations: %v", errors)
	}

	return nil
}

// GetAll retrieves all locations from the repository.
func (repo *InMemoryLocationRepository) GetAll() ([]*entities.Location, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	var locations []*entities.Location
	for _, location := range repo.locations {
		locations = append(locations, location)
	}
	return locations, nil
}

// GetRandomByNetworkType returns a random location with the specified network type.
func (repo *InMemoryLocationRepository) GetRandomByNetworkType(networkType entities.NetworkType) (*entities.Location, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	var locations []*entities.Location
	for _, location := range repo.locations {
		if location.NetworkType == networkType {
			locations = append(locations, location)
		}
	}
	if len(locations) == 0 {
		return nil, errors.New("no locations found for the specified network type")
	}
	rand.Seed(time.Now().UnixNano())
	randomIndex := rand.Intn(len(locations))
	return locations[randomIndex], nil
}
