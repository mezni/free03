package services

import (
	"github.com/mezni/users-go/aggregates"
	"github.com/mezni/users-go/repositories"
)

type PortfolioService struct {
	repo repositories.PortfolioRepository
}

func NewPortfolioService(repo repositories.PortfolioRepository) *PortfolioService {
	return &PortfolioService{repo: repo}
}

func (s *PortfolioService) AddPortfolio(name string) error {
	p, _ := aggregates.NewPortfolio(name)
	s.repo.Create(p)
	return nil
}
