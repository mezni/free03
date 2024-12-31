package inmemstore

import (
    "errors"
    "sync"

    "github.com/mezni/wovoka/cdrgen/domain/entities"
)

// InMemoryNetworkTechnologyRepository is a simple in-memory implementation of NetworkTechnologyRepository.
type InMemoryNetworkTechnologyRepository struct {
    data map[int]entities.NetworkTechnology
    mu   sync.RWMutex
}

// NewInMemoryNetworkTechnologyRepository creates a new instance of InMemoryNetworkTechnologyRepository.
func NewInMemoryNetworkTechnologyRepository() *InMemoryNetworkTechnologyRepository {
    return &InMemoryNetworkTechnologyRepository{
        data: make(map[int]entities.NetworkTechnology),
    }
}

// Create adds a new NetworkTechnology to the repository.
func (r *InMemoryNetworkTechnologyRepository) Create(technology entities.NetworkTechnology) error {
    r.mu.Lock()
    defer r.mu.Unlock()

    if _, exists := r.data[technology.ID]; exists {
        return errors.New("network technology with this ID already exists")
    }

    r.data[technology.ID] = technology
    return nil
}

// GetAll retrieves all NetworkTechnologies.
func (r *InMemoryNetworkTechnologyRepository) GetAll() ([]entities.NetworkTechnology, error) {
    r.mu.RLock()
    defer r.mu.RUnlock()

    technologies := make([]entities.NetworkTechnology, 0, len(r.data))
    for _, tech := range r.data {
        technologies = append(technologies, tech)
    }
    return technologies, nil
}
