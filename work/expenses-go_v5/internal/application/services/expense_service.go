package services

import (
	"errors"
	"github.com/google/uuid"
	"github.com/mezni/expenses-go/internal/domain/entities"
	"github.com/mezni/expenses-go/internal/domain/repositories"
)

type ExpenseService struct {
	orgRepository repositories.OrgRepository
}

func NewProductService(
	orgRepository repositories.OrgRepository
) interfaces.ProductService {
	return &ProductService{productRepository: productRepository, sellerRepository: sellerRepository}
}