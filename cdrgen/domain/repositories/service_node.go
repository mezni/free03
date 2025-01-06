package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

type ServiceNodeRepository interface {
	Insert(serviceNode entities.ServiceNode) error
	GetAll() ([]entities.ServiceNode, error)
}
