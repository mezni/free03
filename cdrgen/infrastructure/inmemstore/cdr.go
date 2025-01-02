package repositories

import (
	"errors"
	"sync"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

type MemoryCDRRepository struct {
	data map[string]domain.CDR
	mu   sync.Mutex
}

func NewMemoryCDRRepository() *MemoryCDRRepository {
	return &MemoryCDRRepository{data: make(map[string]domain.CDR)}
}

func (r *MemoryCDRRepository) Save(cdr domain.CDR) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.data[cdr.ID]; exists {
		return errors.New("CDR already exists")
	}

	r.data[cdr.ID] = cdr
	return nil
}

func (r *MemoryCDRRepository) FindByID(id string) (domain.CDR, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	cdr, exists := r.data[id]
	if !exists {
		return domain.CDR{}, errors.New("CDR not found")
	}
	return cdr, nil
}

func (r *MemoryCDRRepository) FindAll() ([]domain.CDR, error) {
	r.mu.Lock()
	defer r.mu.Unlock()

	cdrs := make([]domain.CDR, 0, len(r.data))
	for _, cdr := range r.data {
		cdrs = append(cdrs, cdr)
	}
	return cdrs, nil
}
