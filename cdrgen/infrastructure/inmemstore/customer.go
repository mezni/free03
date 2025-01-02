package inmemstore

import (
	"errors"
	"math/rand"
	"sync"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

type MemoryCustomerRepository struct {
	customers []domain.Customer
	mu        sync.Mutex
}

func NewMemoryCustomerRepository() *MemoryCustomerRepository {
	return &MemoryCustomerRepository{customers: []domain.Customer{}}
}

func (r *MemoryCustomerRepository) AddCustomer(customer domain.Customer) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.customers = append(r.customers, customer)
}

func (r *MemoryCustomerRepository) FindAll() ([]domain.Customer, error) {
	r.mu.Lock()
	defer r.mu.Unlock()
	if len(r.customers) == 0 {
		return nil, errors.New("no customers available")
	}
	return r.customers, nil
}

func (r *MemoryCustomerRepository) FindRandom() (domain.Customer, error) {
	r.mu.Lock()
	defer r.mu.Unlock()
	if len(r.customers) == 0 {
		return domain.Customer{}, errors.New("no customers available")
	}
	rand.Seed(time.Now().UnixNano())
	return r.customers[rand.Intn(len(r.customers))], nil
}