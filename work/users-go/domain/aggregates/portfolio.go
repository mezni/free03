package aggregates

import (
	"errors"
	"github.com/google/uuid"
	"github.com/mezni/users-go/domain/valueobjects"
	"time"
)

type PortfolioID string

type Portfolio struct {
	ID       PortfolioID
	Name     string
	Limit    *valueobjects.Limit
	ParentID *PortfolioID
}

func (p *Portfolio) validate() error {
	if p.Name == "" {
		return errors.New("name must not be empty")
	}
	if p.Limit.Amount <= 0 {
		return errors.New("price must be greater than 0")
	}
	if p.Limit.CreatedAt.After(p.Limit.UpdatedAt) {
		return errors.New("created_at must be before updated_at")
	}

	return nil
}

func NewPortfolio(name string) (*Portfolio, error) {
	limit := &valueobjects.Limit{
		Amount:    0,
		CreatedAt: time.Now(),
		UpdatedAt: time.Now(),
	}

	return &Portfolio{
		ID:       PortfolioID(uuid.New().String()),
		Name:     name,
		Limit:    limit,
		ParentID: nil,
	}, nil
}

func (p *Portfolio) GetID() PortfolioID {
	return p.ID
}

func (p *Portfolio) SetName(name string) error {
	p.Name = name

	return p.validate()
}

func (p *Portfolio) SetLimit(amount float64) error {
	p.Limit.Amount = amount

	return p.validate()
}
