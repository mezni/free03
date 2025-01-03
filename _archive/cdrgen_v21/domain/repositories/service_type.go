package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// ServiceTypeRepository defines the methods for service type repository.
type ServiceTypeRepository interface {
	Insert(serviceType entities.ServiceType) error
	GetAll() ([]entities.ServiceType, error)
}
