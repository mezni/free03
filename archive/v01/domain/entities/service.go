package entities

import (
	"errors"
)

// Service represents a service.
type Service struct {
	ID          int
	Name        string
	ServiceType string
	Technology  string
	Description string
	RatingID    int
}

// Predefined error messages for validation.
var (
	ErrInvalidID        = errors.New("ID must be a positive integer")
	ErrEmptyName        = errors.New("Name cannot be empty")
	ErrEmptyServiceType = errors.New("ServiceType cannot be empty")
	ErrEmptyTechnology  = errors.New("Technology cannot be empty")
	ErrInvalidRatingID  = errors.New("RatingID cannot be negative")
)

// ServiceFactory is responsible for creating Service instances.
type ServiceFactory struct{}

// NewServiceFactory returns a new ServiceFactory instance.
func NewServiceFactory() *ServiceFactory {
	return &ServiceFactory{}
}

// CreateService creates a new Service object with the given parameters.
func (sf *ServiceFactory) CreateService(id int, name, serviceType, technology, description string, ratingID int) (*Service, error) {
	// Validate parameters
	if id <= 0 {
		return nil, ErrInvalidID
	}
	if name == "" {
		return nil, ErrEmptyName
	}
	if serviceType == "" {
		return nil, ErrEmptyServiceType
	}
	if technology == "" {
		return nil, ErrEmptyTechnology
	}
	if ratingID < 0 {
		return nil, ErrInvalidRatingID
	}

	// Create and return the Service object
	return &Service{
		ID:          id,
		Name:        name,
		ServiceType: serviceType,
		Technology:  technology,
		Description: description,
		RatingID:    ratingID,
	}, nil
}
