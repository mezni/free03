package repositories

import "github.com/mezni/wovoka/configurator/domain/entities"

// LocationRepository defines the methods that a location repository must implement.
type LocationRepository interface {
	Create(location *entities.Location) error
	GetByID(id int) (*entities.Location, error)
	Update(location *entities.Location) error
	Delete(id int) error
	GetAll() ([]*entities.Location, error)
	GetRandomByNetworkType(networkType entities.NetworkType) (*entities.Location, error)
}
