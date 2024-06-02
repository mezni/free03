package entities

import (
	"github.com/google/uuid"
)

type Expense struct {
	ID         uuid.UUID
	ProviderID uuid.UUID
	ServiceID  uuid.UUID
	Amount     float64
}

func NewExpense(providerID uuid.UUID, serviceID uuid.UUID, amount float64) *Expense {
	return &Expense{
		ID:         uuid.New(),
		ProviderID: providerID,
		ServiceID:  serviceID,
		Amount:     amount,
	}
}
