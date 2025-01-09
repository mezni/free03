package inmemstore

import (
	"errors"
	"sort"
	"sync"

	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// InMemCdrRepository is an in-memory implementation of the CdrRepository interface.
type InMemCdrRepository struct {
	data map[int]entities.Cdr
	mu   sync.RWMutex
}

// NewInMemCdrRepository creates a new in-memory repository for CDRs.
func NewInMemCdrRepository() *InMemCdrRepository {
	return &InMemCdrRepository{
		data: make(map[int]entities.Cdr),
	}
}

// Insert adds a new CDR to the repository.
func (r *InMemCdrRepository) Insert(cdr entities.Cdr) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.data[cdr.ID]; exists {
		return errors.New("cdr with the same ID already exists")
	}

	r.data[cdr.ID] = cdr
	return nil
}

// GetAll retrieves all CDRs from the repository.
func (r *InMemCdrRepository) GetAll() ([]entities.Cdr, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	var cdrs []entities.Cdr
	for _, cdr := range r.data {
		cdrs = append(cdrs, cdr)
	}

	return cdrs, nil
}

// GetByID retrieves a CDR by its ID.
func (r *InMemCdrRepository) GetByID(id int) (*entities.Cdr, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	cdr, exists := r.data[id]
	if !exists {
		return nil, errors.New("cdr not found")
	}

	return &cdr, nil
}

// DeleteByID removes a CDR by its ID.
func (r *InMemCdrRepository) DeleteByID(id int) error {
	r.mu.Lock()
	defer r.mu.Unlock()

	if _, exists := r.data[id]; !exists {
		return errors.New("cdr not found")
	}

	delete(r.data, id)
	return nil
}

// GetFirstN retrieves the first N CDRs, sorted by ID.
func (r *InMemCdrRepository) GetFirstN(limit int) ([]entities.Cdr, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	if len(r.data) == 0 {
		return nil, errors.New("no CDRs available")
	}

	// Collect all CDRs into a slice
	var cdrs []entities.Cdr
	for _, cdr := range r.data {
		cdrs = append(cdrs, cdr)
	}

	// Sort CDRs by ID
	sort.Slice(cdrs, func(i, j int) bool {
		return cdrs[i].ID < cdrs[j].ID
	})

	// Return the first N CDRs (or fewer if there aren't N)
	if len(cdrs) > limit {
		return cdrs[:limit], nil
	}
	return cdrs, nil
}

// Length returns the total number of CDR records in the in-memory repository.
func (repo *InMemCdrRepository) Length() (int, error) {
	repo.mu.RLock() // Use RLock for reading
	defer repo.mu.RUnlock()
	return len(repo.data), nil // Corrected to use repo.data
}
