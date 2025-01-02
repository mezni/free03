package repositories

import (
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// CustomerRepository defines methods for accessing customer data.
type CustomerRepository interface {
	FindAll() ([]Customer, error)
	FindRandom() (Customer, error)
}
