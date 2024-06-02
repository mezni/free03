package entities

import (
	"github.com/google/uuid"
)

type Expense struct {
	ID        uuid.UUID
	ServiceID uuid.UUID
	Amount    float64
}

func NewExpense(serviceID uuid.UUID, amount float64) *Expense {
	return &Expense{
		ID:        uuid.New(),
		ServiceID: serviceID,
		Amount:    amount,
	}
}
