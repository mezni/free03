package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkTechnologyRepository defines the methods for network technology repository.
type NetworkTechnologyRepository interface {
	Insert(networkTechnology entities.NetworkTechnology) error
	GetAll() ([]entities.NetworkTechnology, error)
}
