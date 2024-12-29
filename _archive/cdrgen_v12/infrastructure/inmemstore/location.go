package inmemstore

import (
    "errors"
    "math/rand"
    "sync"
    "time"
    "github.com/mezni/wovoka/cdrgen/domain/entities"
)

type InMemoryLocationRepository struct {
    locations map[int]*entities.Location
    nextID    int
    mu        sync.RWMutex
}

func NewInMemoryLocationRepository() *InMemoryLocationRepository {
    // Seed the random number generator once
    rand.Seed(time.Now().UnixNano())
    return &InMemoryLocationRepository{
        locations: make(map[int]*entities.Location),
        nextID:    1,
    }
}

// Create adds a new Location to the repository.
func (r *InMemoryLocationRepository) Create(location *entities.Location) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    location.ID = r.nextID
    r.locations[r.nextID] = location
    r.nextID++
    return nil
}

// Get retrieves a Location by its ID.
func (r *InMemoryLocationRepository) Get(id int) (*entities.Location, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    location, exists := r.locations[id]
    if !exists {
        return nil, errors.New("location not found")
    }
    return location, nil
}

// GetAll retrieves all Locations from the repository.
func (r *InMemoryLocationRepository) GetAll() ([]*entities.Location, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    allLocations := make([]*entities.Location, 0, len(r.locations))
    for _, location := range r.locations {
        allLocations = append(allLocations, location)
    }
    return allLocations, nil
}

// GetRandomByNetworkTechnology retrieves a random Location by network technology.
func (r *InMemoryLocationRepository) GetRandomByNetworkTechnology(networkTechnology string) (*entities.Location, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    var filteredLocations []*entities.Location
    for _, location := range r.locations {
        if location.NetworkTechnology == networkTechnology {
            filteredLocations = append(filteredLocations, location)
        }
    }

    if len(filteredLocations) == 0 {
        return nil, errors.New("no locations found for the specified network technology")
    }

    randomIndex := rand.Intn(len(filteredLocations))
    return filteredLocations[randomIndex], nil
}
