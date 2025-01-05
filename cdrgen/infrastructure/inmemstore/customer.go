package inmemstore

import (
	"errors"
	"sync"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// InMemCustomerRepository is an in-memory implementation of CustomerRepository.
type InMemCustomerRepository struct {
	data map[int]entities.Customer
	mu   sync.RWMutex
}

// NewInMemCustomerRepository creates a new in-memory repository instance for customers.
func NewInMemCustomerRepository() *InMemCustomerRepository {
	return &InMemCustomerRepository{
		data: make(map[int]entities.Customer),
	}
}

// Insert adds a new Customer to the repository.
func (repo *InMemCustomerRepository) Insert(customer entities.Customer) error {
	repo.mu.Lock()
	defer repo.mu.Unlock()

	if _, exists := repo.data[customer.ID]; exists {
		return errors.New("customer with the same ID already exists")
	}

	repo.data[customer.ID] = customer
	return nil
}

// GetAll retrieves all Customer entities from the repository.
func (repo *InMemCustomerRepository) GetAll() ([]entities.Customer, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	var customers []entities.Customer
	for _, customer := range repo.data {
		customers = append(customers, customer)
	}

	return customers, nil
}
