package aggregate

import (
	"github.com/mezni/users-go/entity"
	"github.com/mezni/users-go/valueobject"
)

type Customer struct {
	person       *entity.Person
	products     []*entity.Item
	transactions []*valueobject.Transaction
}
