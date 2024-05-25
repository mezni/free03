package main

import (
	"fmt"
	"github.com/google/uuid"
	"time"
)

type Portfolio struct {
	ID        uuid.UUID
	Name      string
	Limit     float64
	OwnerID   uuid.UUID
	ParentID  *uuid.UUID
	CreatedAt time.Time
	UpdatedAt time.Time
}

func NewPortfolio(name string, ownerID uuid.UUID, parentID *uuid.UUID) *Portfolio {
	return &Portfolio{
		ID:        uuid.New(),
		Name:      name,
		Limit:     0,
		OwnerID:   ownerID,
		ParentID:  parentID,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}
}

func (p *Portfolio) UpdateName(name string) error {
	p.Name = name
	p.UpdatedAt = time.Now()

	return nil
}

func (p *Portfolio) UpdateLimit(limit float64) error {
	p.Limit = limit
	p.UpdatedAt = time.Now()

	return nil
}

func main() {
	fmt.Println("Start")
	p := NewPortfolio("Test", uuid.New(), nil)
	fmt.Println(p)
	_ = p.UpdateName("Test1")
	fmt.Println(p)
	_ = p.UpdateLimit(12)
	fmt.Println(p)
}
