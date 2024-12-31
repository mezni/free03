package repositories

import 	"github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkTechnologyRepository defines methods to manage NetworkTechnologies.
type NetworkTechnologyRepository interface {
    Create(technology entities.NetworkTechnology) error
    GetAll() ([]entities.NetworkTechnology, error)
}