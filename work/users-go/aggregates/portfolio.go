package aggregates

import (
	//	"errors"
	"github.com/google/uuid"
	"github.com/mezni/users-go/valueobjects"
	"time"
)

type Portfolio struct {
	ID       uuid.UUID
	Name     string
	Limit    *valueobjects.Limit
	ParentID *uuid.UUID
}

func NewPortfolio(name string) (*Portfolio, error) {
	limit := &valueobjects.Limit{
		Limit:     0,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	return &Portfolio{
		ID:       uuid.New(),
		Name:     name,
		Limit:    limit,
		ParentID: nil,
	}, nil
}
