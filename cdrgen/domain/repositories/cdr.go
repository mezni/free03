package service

import (
	"errors"
	"fmt"
	"sync"
	"time"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// CDRRepository defines the interface for interacting with the CDR storage.
type CDRRepository interface {
	Save(cdr entities.CDR) error
	FindByID(id string) (entities.CDR, error)
	FindAll() ([]entities.CDR, error)
}

