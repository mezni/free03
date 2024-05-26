package repositories

import (
	//	"fmt"
	"github.com/mezni/users-go/domain"
)

type PortfolioRepository interface {
	Save(user *entities.Portfolio) error
}
