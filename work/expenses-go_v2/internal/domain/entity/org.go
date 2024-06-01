package domain

import (
	"github.com/google/uuid"
)

type Org struct {
	ID   uuid.UUID
	Name string
}

func NewOrg(name string) *Org {
	return &Order{
		ID:   uuid.New(),
		Name: name,
	}
}
