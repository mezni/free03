package domain

import (
	"github.com/google/uuid"
)

type OrgRepository interface {
	Save(org *Org) error
	FindByID(id uuid.UUID) (*Org, error)
	FindByName(name string) (*Org, error)
}
