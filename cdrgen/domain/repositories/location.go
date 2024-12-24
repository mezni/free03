package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// LocationRepository defines the interface for any location repository (e.g., in-memory, BoltDB, etc.).
type LocationRepository interface {
	// Create inserts a new location into the repository.
	Create(location *entities.Location) error
	
	// CreateMultiple inserts multiple locations into the repository.
	CreateMultiple(locations []*entities.Location) error
	
	// GetAll retrieves all locations from the repository.
	GetAll() ([]*entities.Location, error)
	
	// GetRandomByNetworkType returns a random location filtered by network type.
	GetRandomByNetworkType(networkType entities.NetworkType) (*entities.Location, error)
}
