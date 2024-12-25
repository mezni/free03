package inmem

import (
	"errors"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
)

// InMemoryNetworkElementRepo represents an in-memory repository for NetworkElements.
type InMemoryNetworkElementRepo struct {
	data map[int]*entities.NetworkElement
}

// NewInMemoryNetworkElementRepo creates a new in-memory repository.
func NewInMemoryNetworkElementRepo() *InMemoryNetworkElementRepo {
	return &InMemoryNetworkElementRepo{
		data: make(map[int]*entities.NetworkElement),
	}
}

// Create adds a new NetworkElement to the repository.
func (repo *InMemoryNetworkElementRepo) Create(ne *entities.NetworkElement) error {
	if _, exists := repo.data[ne.NetworkElementTypeID]; exists {
		return errors.New("NetworkElement with ID already exists")
	}
	repo.data[ne.NetworkElementTypeID] = ne
	return nil
}

// CreateMultiple adds multiple NetworkElements to the repository.
func (repo *InMemoryNetworkElementRepo) CreateMultiple(neList []*entities.NetworkElement) error {
	for _, ne := range neList {
		if err := repo.Create(ne); err != nil {
			return err
		}
	}
	return nil
}

// GetAll returns all NetworkElements in the repository.
func (repo *InMemoryNetworkElementRepo) GetAll() ([]*entities.NetworkElement, error) {
	var elements []*entities.NetworkElement
	for _, ne := range repo.data {
		elements = append(elements, ne)
	}
	return elements, nil
}

// GetRandomByNetworkType returns a random NetworkElement of the specified NetworkType.
func (repo *InMemoryNetworkElementRepo) GetRandomByNetworkType(nt entities.NetworkType) (*entities.NetworkElement, error) {
	var matchingElements []*entities.NetworkElement
	for _, ne := range repo.data {
		if ne.NetworkType == nt {
			matchingElements = append(matchingElements, ne)
		}
	}
	if len(matchingElements) == 0 {
		return nil, errors.New("No NetworkElement found for the given NetworkType")
	}
	// Logic to return a random element from matchingElements
	return matchingElements[0], nil
}
