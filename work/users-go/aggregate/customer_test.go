package aggregate_test

import "testing"

func TestCustomer_NewCustomer(t *testing.T) {
	if name == "" {
		return Customer{}, ErrInvalidPerson
	}
	person := &Person{Name: name, ID: uuid.New()}
	return Customer{
		person:       person,
		products:     make([]*entity.Item, 0),
		transactions: make([]valueobject.Transaction, 0),
	}, nil
}
