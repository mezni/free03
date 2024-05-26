package entities

import (
	"github.com/google/uuid"
	// "time"
)

type PortfolioID string

type Portfolio struct {
	ID       PortfolioID
	Name     string
	Limit    float64
	ParentID PortfolioID
	// CreatedAt time.Time
	// UpdatedAt time.Time
}

func NewPortfolio(name string, limit float64) *Portfolio {
	return &Portfolio{
		ID:       PortfolioID(uuid.New().String()),
		Name:     name,
		Limit:    0,
		ParentID: "",
		//		CreatedAt: time.Now(),
		//		UpdatedAt: time.Now(),
	}
}

func (p *Portfolio) UpdateName(name string) error {
	p.Name = name
	//	p.UpdatedAt = time.Now()

	// return p.validate()
	return nil
}
