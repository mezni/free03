

package repositories

import (
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)


type NetworkElementTypeRepository interface {
	Save(elementType entities.NetworkElementType) error
	GetAll() ([]entities.NetworkElementType, error)
}



