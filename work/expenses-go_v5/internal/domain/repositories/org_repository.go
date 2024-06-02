package repositories

import (
	"github.com/google/uuid"
	"github.com/mezni/expenses-go/internal/domain/entities"
)



type OrgRepository interface {
    FindByName(name string) (*entities.Org, error)
}