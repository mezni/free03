package entities

import (
	"github.com/google/uuid"
)

type Service struct {
	ID   uuid.UUID
	Name string
	ProviderID uuid.UUID
}

func NewService(name string,providerID uuid.UUID) *Service {
	return &Service{
		ID:   uuid.New(),
		Name: name,
		ProviderID: providerID
	}
}
