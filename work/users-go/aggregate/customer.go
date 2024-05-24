package aggregate

import (
	"github.com/google/uuid"
	"github.com/mezni/users-go/entity"
	"github.com/mezni/users-go/valueobject"
)

var (
	ErrInvalidPerson = errors.New("a customer has to have a valid name")
)

type Customer struct {
	person       *entity.Person
	products     []*entity.Item
	transactions []valueobject.Transaction
}

func NewCustomer(name string) (Customer, error) {
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
