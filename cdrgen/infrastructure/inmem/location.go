package inmemorystore

import (
	"errors"
	"math/rand"
	"time"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// InMemoryLocationRepository is an in-memory implementation of the LocationRepository.
type InMemoryLocationRepository struct {
	locations map[int]*entities.Location
}

// NewInMemoryLocationRepository creates a new instance of InMemoryLocationRepository.
func NewInMemoryLocationRepository() *InMemoryLocationRepository {
	return &InMemoryLocationRepository{
		locations: make(map[int]*entities.Location),
	}
}

// Create inserts a location into the repository.
func (repo *InMemoryLocationRepository) Create(location *entities.Location) error {
	if _, exists := repo.locations[location.LocationID]; exists {
		return errors.New("location with this ID already exists")
	}
	repo.locations[location.LocationID] = location
	return nil
}

// CreateMultiple inserts multiple locations into the repository.
func (repo *InMemoryLocationRepository) CreateMultiple(locations []*entities.Location) error {
	for _, location := range locations {
		if _, exists := repo.locations[location.LocationID]; exists {
			return errors.New("one or more locations already exist")
		}
		repo.locations[location.LocationID] = location
	}
	return nil
}

// GetAll retrieves all locations from the repository.
func (repo *InMemoryLocationRepository) GetAll() ([]*entities.Location, error) {
	var locations []*entities.Location
	for _, location := range repo.locations {
		locations = append(locations, location)
	}
	return locations, nil
}

// GetRandomByNetworkType returns a random location with the specified network type.
func (repo *InMemoryLocationRepository) GetRandomByNetworkType(networkType entities.NetworkType) (*entities.Location, error) {
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
