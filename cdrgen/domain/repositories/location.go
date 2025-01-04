package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkElementTypeRepository defines the methods for network element type repository.
type LocationRepository interface {
	Insert(location entities.Location) error
	GetAll() ([]entities.Location, error)
}