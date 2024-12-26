package repositories

import "github.com/mezni/wovoka/cdrgen/internal/domain/entities"

// NetworkTechnologyRepository defines the methods that any repository for NetworkTechnology must implement.
type NetworkTechnologyRepository interface {
	// Save a NetworkTechnology entity
	Save(networkTechnology entities.NetworkTechnology) error

	// FindAll retrieves all NetworkTechnology entities
	FindAll() ([]entities.NetworkTechnology, error)

	// FindByID retrieves a NetworkTechnology by its ID
	FindByID(id string) (entities.NetworkTechnology, error)

	// Delete removes a NetworkTechnology by its ID
	Delete(id string) error
}
