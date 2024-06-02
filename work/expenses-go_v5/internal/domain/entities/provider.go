package entities

import (
	"github.com/google/uuid"
)

type Provider struct {
	ID   uuid.UUID
	Name string
}

func NewProvider(name string) *Provider {
	return &Provider{
		ID:   uuid.New(),
		Name: name,
	}
}
