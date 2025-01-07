package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkElementTypeRepository defines the methods for network element type repository.
type NetworkElementRepository interface {
	Insert(networkElement entities.NetworkElement) error
	GetAll() ([]entities.NetworkElement, error)
}
