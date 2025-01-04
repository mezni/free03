package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

type ServiceTypeRepository interface {
	Insert(serviceType entities.ServiceType) error
	GetAll() ([]entities.ServiceType, error)
}
