package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// ServiceTypeRepository defines the interface for service type operations.
type ServiceTypeRepository interface {
	Insert(serviceType entities.ServiceType) error
	GetAll() ([]entities.ServiceType, error)
	GetByNetworkTechnologyAndName(networkTechnology, name string) (entities.ServiceType, error)
}
