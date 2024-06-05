package services

import (
	"fmt"
	//    "github.com/google/uuid"
	//	"github.com/mezni/expenses-go/internal/domain/entities"
	"github.com/mezni/expenses-go/internal/domain/repositories"
)

type ExpenseService struct {
	repo repositories.OrgRepository
}

func NewExpenseService(repo repositories.OrgRepository) *ExpenseService {
	return &ExpenseService{repo: repo}
}

func (s *ExpenseService) Load() error {
	org, err := s.repo.FindByName("phonix")
	fmt.Println(org, err)
	return err

}
