package repositories

import (
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// NetworkElementRepository defines methods for accessing network elements.
type NetworkElementRepository interface {
	FindAll() ([]NetworkElement, error)
	FindRandom() (NetworkElement, error)
}
