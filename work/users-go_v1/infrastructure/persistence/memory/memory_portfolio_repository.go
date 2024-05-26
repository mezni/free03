package memory

import (
	"errors"
	"github.com/google/uuid"
	"github.com/mezni/users-go/domain"
	"sync"
)

type InMemoryPortfolioRepository struct {
	portfolios map[uuid.UUID]*entities.Portfolio
	mu         sync.RWMutex
}

func NewInMemoryPortfolioRepository() *InMemoryPortfolioRepository {
	return &InMemoryPortfolioRepository{
		portfolios: make(map[uuid.UUID]*entities.Portfolio),
	}
}
