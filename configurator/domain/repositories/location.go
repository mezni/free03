package repositories

import "github.com/mezni/wovoka/configurator/domain/entities"

// LocationRepository defines the methods for interacting with Location data.
type LocationRepository interface {
	// Create a new location.
	Create(location *entities.Location) error

	// Get a location by its ID.
	GetByID(id int) (*entities.Location, error)

	// Update an existing location.
	Update(location *entities.Location) error

	// Delete a location by its ID.
	Delete(id int) error

	// Get all locations.
	GetAll() ([]*entities.Location, error)
}
