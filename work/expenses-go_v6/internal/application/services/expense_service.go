package services

import (
	"github.com/google/uuid"
	"github.com/mezni/expenses-go/internal/domain/repositories"
)

type ExpenseService struct {
	orgRepository repositories.OrgRepository
}

func NewExpenseService(
	orgRepository repositories.OrgRepository,
) interfaces.ProductService {
	return &ExpenseService{orgRepository: orgRepository}
}
