package inmemorystore

import (
	"github.com/mezni/wovoka/configurator/domain/entities"
	"fmt"
)

// InMemoryLocationRepository implements the LocationRepository interface for in-memory storage.
type InMemoryLocationRepository struct {
	locations map[int]*entities.Location
}

// NewInMemoryLocationRepository creates a new in-memory location repository.
func NewInMemoryLocationRepository() *InMemoryLocationRepository {
	return &InMemoryLocationRepository{
		locations: make(map[int]*entities.Location),
	}
}

// Create a new location in the in-memory repository.
func (repo *InMemoryLocationRepository) Create(location *entities.Location) error {
	if _, exists := repo.locations[location.LocationID]; exists {
		return fmt.Errorf("location with this ID already exists")
	}
	repo.locations[location.LocationID] = location
	return nil
}

// GetByID retrieves a location by its ID.
func (repo *InMemoryLocationRepository) GetByID(id int) (*entities.Location, error) {
	location, exists := repo.locations[id]
	if !exists {
		return nil, fmt.Errorf("location not found")
	}
	return location, nil
}

// Update an existing location.
func (repo *InMemoryLocationRepository) Update(location *entities.Location) error {
	if _, exists := repo.locations[location.LocationID]; !exists {
		return fmt.Errorf("location not found")
	}
	repo.locations[location.LocationID] = location
	return nil
}

// Delete a location by its ID.
func (repo *InMemoryLocationRepository) Delete(id int) error {
	if _, exists := repo.locations[id]; !exists {
		return fmt.Errorf("location not found")
	}
	delete(repo.locations, id)
	return nil
}

// GetAll retrieves all locations.
func (repo *InMemoryLocationRepository) GetAll() ([]*entities.Location, error) {
	var allLocations []*entities.Location
	for _, location := range repo.locations {
		allLocations = append(allLocations, location)
	}
	return allLocations, nil
}

// GetRandomByNetworkType retrieves a random location for a given network type.
func (repo *InMemoryLocationRepository) GetRandomByNetworkType(networkType entities.NetworkType) (*entities.Location, error) {
	var matchingLocations []*entities.Location
	for _, location := range repo.locations {
		if location.NetworkType == networkType {
			matchingLocations = append(matchingLocations, location)
		}
	}

	if len(matchingLocations) == 0 {
		return nil, fmt.Errorf("no locations found for network type %v", networkType)
	}

	// For simplicity, just return the first matching location.
	// In a real application, you could randomize the selection.
	return matchingLocations[0], nil
}
