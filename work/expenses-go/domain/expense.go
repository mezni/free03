package domain

import (
	"github.com/google/uuid"
)

type Service struct {
	ID   uuid.UUID
	Name string
}

type Expense struct {
	ID          uuid.UUID
	ServiceName uuid.UUID
	Amount      float64
}
