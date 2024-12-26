package repositories

import "github.com/mezni/wovoka/cdrgen/internal/domain/repositories"

// NetworkTechnologyRepository defines the methods that any repository for NetworkTechnology must implement.
type NetworkTechnologyRepository interface {
	// Save a NetworkTechnology entity
	Save(networkTechnology domain.NetworkTechnology) error

	// FindAll retrieves all NetworkTechnology entities
	FindAll() ([]domain.NetworkTechnology, error)

	// FindByID retrieves a NetworkTechnology by its ID
	FindByID(id string) (domain.NetworkTechnology, error)

	// Delete removes a NetworkTechnology by its ID
	Delete(id string) error
}
