package entities

import (
	"github.com/google/uuid"
)

type Service struct {
	ID         uuid.UUID
	ProviderID uuid.UUID
	Name       string
}

func NewService(name string, providerID uuid.UUID) *Service {
	return &Service{
		ID:         uuid.New(),
		ProviderID: providerID,
		Name:       name,
	}
}
