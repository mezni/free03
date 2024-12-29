package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// LocationRepository defines the methods for interacting with the location data store.
type LocationRepository interface {
	Save(location *entities.Location) error
	GetByID(id int) (*entities.Location, error)
}
