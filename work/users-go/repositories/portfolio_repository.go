package repositories

import (
	"github.com/mezni/users-go/aggregates"
)

type PortfolioRepository interface {
	Create(portfolio *aggregates.Portfolio) error
}
