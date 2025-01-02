package repositories

import (
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)


type NetworkTechnologyRepository interface {
	Save(technology models.NetworkTechnology) error
	GetAll() ([]models.NetworkTechnology, error)
}



