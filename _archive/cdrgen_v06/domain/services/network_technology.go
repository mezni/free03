package services

import (
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/repositories"
)

type NetworkTechnologyService struct {
	repo repositories.NetworkTechnologyRepository
}

// NewNetworkTechnologyService creates a new service instance for NetworkTechnology.
func NewNetworkTechnologyService(repo repositories.NetworkTechnologyRepository) *NetworkTechnologyService {
	return &NetworkTechnologyService{
		repo: repo,
	}
}

// Create inserts a new NetworkTechnology into the repository.
func (s *NetworkTechnologyService) Create(tech entities.NetworkTechnology) (entities.NetworkTechnology, error) {
	// Check if technology already exists by name
	existingTech, found, err := s.repo.FindByName(tech.Name)
	if err != nil {
		return entities.NetworkTechnology{}, fmt.Errorf("error checking if technology exists: %w", err)
	}
	if found {
		return entities.NetworkTechnology{}, fmt.Errorf("network technology with name '%s' already exists", existingTech.Name)
	}

	// Create new technology in the repository
	return s.repo.Create(tech)
}

// CreateMany creates multiple NetworkTechnologies.
func (s *NetworkTechnologyService) CreateMany(technologies []entities.NetworkTechnology) ([]entities.NetworkTechnology, error) {
	var createdTechnologies []entities.NetworkTechnology
	for _, tech := range technologies {
		createdTech, err := s.Create(tech)
		if err != nil {
			return nil, fmt.Errorf("failed to create technology: %w", err)
		}
		createdTechnologies = append(createdTechnologies, createdTech)
	}
	return createdTechnologies, nil
}

// FindAll retrieves all NetworkTechnologies from the repository.
func (s *NetworkTechnologyService) FindAll() ([]entities.NetworkTechnology, error) {
	return s.repo.FindAll()
}
