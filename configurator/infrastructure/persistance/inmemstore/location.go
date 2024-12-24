package inmemorystore

import (
	"errors"
	"github.com/mezni/wovoka/configurator/domain/entities"
)

// InMemoryLocationRepository is an in-memory implementation of the LocationRepository interface.
type InMemoryLocationRepository struct {
	locations map[int]*entities.Location
}

// NewInMemoryLocationRepository creates a new in-memory repository.
func NewInMemoryLocationRepository() *InMemoryLocationRepository {
	return &InMemoryLocationRepository{
		locations: make(map[int]*entities.Location),
	}
}

// Create a new location in the repository.
func (repo *InMemoryLocationRepository) Create(location *entities.Location) error {
	if _, exists := repo.locations[location.LocationID]; exists {
		return errors.New("location with this ID already exists")
	}
	repo.locations[location.LocationID] = location
	return nil
}

// Get a location by its ID.
func (repo *InMemoryLocationRepository) GetByID(id int) (*entities.Location, error) {
	location, exists := repo.locations[id]
	if !exists {
		return nil, errors.New("location not found")
	}
	return location, nil
}

// Update an existing location in the repository.
func (repo *InMemoryLocationRepository) Update(location *entities.Location) error {
	if _, exists := repo.locations[location.LocationID]; !exists {
		return errors.New("location not found")
	}
	repo.locations[location.LocationID] = location
	return nil
}

// Delete a location by its ID.
func (repo *InMemoryLocationRepository) Delete(id int) error {
	if _, exists := repo.locations[id]; !exists {
		return errors.New("location not found")
	}
	delete(repo.locations, id)
	return nil
}

// Get all locations from the repository.
func (repo *InMemoryLocationRepository) GetAll() ([]*entities.Location, error) {
	allLocations := []*entities.Location{}
	for _, location := range repo.locations {
		allLocations = append(allLocations, location)
	}
	return allLocations, nil
}
