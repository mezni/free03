package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// NetworkTechnologyRepository defines the methods for network technology repository.
type CustomerRepository interface {
	Insert(customer entities.Customer) error
	GetAll() ([]entities.Customer, error)
}
