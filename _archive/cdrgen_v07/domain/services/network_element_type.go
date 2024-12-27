package services

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/repositories"
)

type NetworkElementTypeService struct {
	repo repositories.NetworkElementTypeRepository
}

// NewNetworkElementTypeService creates a new service instance for NetworkElementType.
func NewNetworkElementTypeService(repo repositories.NetworkElementTypeRepository) *NetworkElementTypeService {
	return &NetworkElementTypeService{
		repo: repo,
	}
}

// Create inserts a new NetworkElementType into the repository.
func (s *NetworkElementTypeService) Create(element entities.NetworkElementType) (entities.NetworkElementType, error) {
	// Check if element type already exists by name
	existingElement, found, err := s.repo.FindByName(element.Name)
	if err != nil {
		return entities.NetworkElementType{}, fmt.Errorf("error checking if element exists: %w", err)
	}
	if found {
		return entities.NetworkElementType{}, fmt.Errorf("network element type with name '%s' already exists", existingElement.Name)
	}

	// Create new element in the repository
	return s.repo.Create(element)
}

// CreateMany creates multiple NetworkElementTypes.
func (s *NetworkElementTypeService) CreateMany(elements []entities.NetworkElementType) ([]entities.NetworkElementType, error) {
	var createdElements []entities.NetworkElementType
	for _, element := range elements {
		createdElement, err := s.Create(element)
		if err != nil {
			return nil, fmt.Errorf("failed to create element type: %w", err)
		}
		createdElements = append(createdElements, createdElement)
	}
	return createdElements, nil
}

// FindAll retrieves all NetworkElementTypes from the repository.
func (s *NetworkElementTypeService) FindAll() ([]entities.NetworkElementType, error) {
	return s.repo.FindAll()
}
