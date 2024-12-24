package interfaces

import "github.com/mezni/wovoka/domain/entities"

// ServiceRepository defines operations for managing Service entities.
type ServiceRepository interface {
	// Create a new Service
	Create(service *entities.Service) error

	// Get a Service by ID
	GetByID(id int) (*entities.Service, error)

	// Get a Service by Name
	GetByName(name string) (*entities.Service, error)

	// Update an existing Service
	Update(service *entities.Service) error

	// Delete a Service by ID
	Delete(id int) error

	// List all Services
	List() ([]*entities.Service, error)
}
