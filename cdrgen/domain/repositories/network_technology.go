package repositories

import (
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)


type NetworkTechnologyRepository interface {
	Save(technology entities.NetworkTechnology) error
	GetAll() ([]entities.NetworkTechnology, error)
}



