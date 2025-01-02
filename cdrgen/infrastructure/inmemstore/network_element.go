package repositories

import (
	"errors"
	"math/rand"
	"sync"
	"time"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

type MemoryNetworkElementRepository struct {
	elements []domain.NetworkElement
	mu       sync.Mutex
}

func NewMemoryNetworkElementRepository() *MemoryNetworkElementRepository {
	return &MemoryNetworkElementRepository{elements: []domain.NetworkElement{}}
}

func (r *MemoryNetworkElementRepository) AddNetworkElement(element domain.NetworkElement) {
	r.mu.Lock()
	defer r.mu.Unlock()
	r.elements = append(r.elements, element)
}

func (r *MemoryNetworkElementRepository) FindAll() ([]domain.NetworkElement, error) {
	r.mu.Lock()
	defer r.mu.Unlock()
	if len(r.elements) == 0 {
		return nil, errors.New("no network elements available")
	}
	return r.elements, nil
}

func (r *MemoryNetworkElementRepository) FindRandom() (domain.NetworkElement, error) {
	r.mu.Lock()
	defer r.mu.Unlock()
	if len(r.elements) == 0 {
		return domain.NetworkElement{}, errors.New("no network elements available")
	}
	rand.Seed(time.Now().UnixNano())
	return r.elements[rand.Intn(len(r.elements))], nil
}
