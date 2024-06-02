package repositories

import (
	"github.com/google/uuid"
	"github.com/mezni/expenses-go/domain/entities"
)

type ServiceRepository interface {
	Create(service *entities.Service) (*entities.Service, error)
	FindById(id uuid.UUID) (*entities.Service, error)
	FindByName(name string) (*entities.Service, error)
}