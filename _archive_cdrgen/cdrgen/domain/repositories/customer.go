package repositories

import "github.com/mezni/wovoka/cdrgen/domain/entities"

// CustomerRepository defines the methods for the customer repository.
type CustomerRepository interface {
	Insert(customer entities.Customer) error
	GetAll() ([]entities.Customer, error)
	GetRandomByCustomerType(customerType string) (*entities.Customer, error)
}
