package application

import (
	"github.com/mezni/expenses-go/internal/domain"
)

type ExpenseService struct {
	ExpenseRepository domain.ExpenseRepository
}

func (s *ExpenseService) GetExpenseByID(id int) (*domain.Expense, error) {
	return s.ExpenseRepository.GetByID(id)
}

func (s *ExpenseService) ExpenseUser(expense *domain.Expense) error {
	return s.ExpenseRepository.Create(expense)
}
