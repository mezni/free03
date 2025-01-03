package repositories

import "github.com/mezni/wovoka/cdrgen/entities"

// NetworkElementTypeRepository defines the methods for network element type repository.
type NetworkElementTypeRepository interface {
	Insert(networkElementType entities.NetworkElementType) error
	GetAll() ([]entities.NetworkElementType, error)
}