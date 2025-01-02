package repositories

import (
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

type CDRRepository interface {
	Save(cdr CDR) error
	FindByID(id string) (CDR, error)
	FindAll() ([]CDR, error)
}
