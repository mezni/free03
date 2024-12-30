package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkTechnologyRepository defines the interface for repository operations on NetworkTechnology entities.
type NetworkTechnologyRepository interface {
	// Save saves a new network technology or updates an existing one.
	Save(networkTechnology *entities.NetworkTechnology) error


	// FindAll retrieves all network technologies.
	FindAll() ([]*entities.NetworkTechnology, error)
}