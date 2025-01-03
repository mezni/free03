package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkTechnologyRepository defines the methods for network technology repository.
type LocationRepository interface {
	Insert(location entities.Location) error
	GetAll() ([]entities.Location, error)
}
