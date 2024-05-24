package aggregates

import (
	"github.com/google/uuid"
	"time"
)

type Portfolio struct {
	ID        uuid.UUID
	Name      string
	OwnerID   uuid.UUID
	ParentID  uuid.UUID
	CreatedAt time.Time
	UpdatedAt time.Time
}

func NewPortfolio(name string, ownerID uuid.UUID, parentID uuid.UUID) *Portfolio {
	return &Portfolio{
		ID:        uuid.New(),
		Name:      name,
		OwnerID:   ownerID,
		ParentID:  parentID,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
}
