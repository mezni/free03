package interfaces

import (
	"github.com/google/uuid"
	"github.com/mezni/expenses-go/internal/application/queries"
)

type ExpenseService interface {
	FindOrgByName(id uuid.UUID) (*queries.OrgQueryResult, error)
}
