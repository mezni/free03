package inmemstore

import (
	"errors"
	"math/rand"
	"sync"
	"time"

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

// GetRandomByCustomerType retrieves a random customer of a specified type.
func (repo *InMemCustomerRepository) GetRandomByCustomerType(customerType string) (*entities.Customer, error) {
	repo.mu.RLock()
	defer repo.mu.RUnlock()

	// Collect customers matching the type
	var matchingCustomers []entities.Customer
	for _, customer := range repo.data {
		if customer.CustomerType == customerType {
			matchingCustomers = append(matchingCustomers, customer)
		}
	}

	// Return error if no matching customers found
	if len(matchingCustomers) == 0 {
		return nil, errors.New("no customers found for the given customer type")
	}

	// Seed random generator and pick a random customer
	rand.Seed(time.Now().UnixNano())
	randomIndex := rand.Intn(len(matchingCustomers))

	return &matchingCustomers[randomIndex], nil
}
