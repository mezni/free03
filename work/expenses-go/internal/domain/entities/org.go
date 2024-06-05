package entities

import (
	"github.com/google/uuid"
)

type Org struct {
	ID   uuid.UUID
	Name string
}

func NewOrg(name string) *Org {
	return &Org{
		ID:   uuid.New(),
		Name: name,
	}
}
