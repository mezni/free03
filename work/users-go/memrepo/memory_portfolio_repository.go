package memory_repo

import (
	"github.com/google/uuid"
	"github.com/mezni/users-go/aggregates"
)

type InMemoryPortfolioRepository struct {
	portfolios map[uuid.UUID]*aggregates.Portfolio
}

func NewInMemoryPortfolioRepository() *InMemoryPortfolioRepository {
	return &InMemoryPortfolioRepository{portfolios: make(map[uuid.UUID]*aggregates.Portfolio)}
}

func (r *InMemoryPortfolioRepository) Create(p *aggregates.Portfolio) error {
	r.portfolios[p.ID] = p
	return nil
}
