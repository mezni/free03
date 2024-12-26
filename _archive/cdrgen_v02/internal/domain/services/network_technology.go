package service

import (
	"errors"

	"github.com/mezni/wovoka/cdrgen/internal/domain/entities"
	"github.com/mezni/wovoka/cdrgen/internal/domain/repositories"
)

// NetworkTechnologyService provides business logic for network technologies
type NetworkTechnologyService struct {
	repo repositories.NetworkTechnologyRepository
}

// NewNetworkTechnologyService creates a new service instance
func NewNetworkTechnologyService(repo repositories.NetworkTechnologyRepository) *NetworkTechnologyService {
	return &NetworkTechnologyService{repo: repo}
}

// SaveNetworkTechnology validates and saves a network technology
func (s *NetworkTechnologyService) SaveNetworkTechnology(nt entities.NetworkTechnology) error {
	if err := s.validateNetworkTechnology(nt); err != nil {
		return err
	}

	// Call repository to save the entity
	return s.repo.Save(nt)
}

// GetNetworkTechnologyByID retrieves a network technology by ID
func (s *NetworkTechnologyService) GetNetworkTechnologyByID(id string) (entities.NetworkTechnology, error) {
	if id == "" {
		return entities.NetworkTechnology{}, errors.New("network technology ID cannot be empty")
	}

	// Call repository to fetch the entity by ID
	return s.repo.FindByID(id)
}

// ListNetworkTechnologies retrieves all saved network technologies
func (s *NetworkTechnologyService) ListNetworkTechnologies() ([]entities.NetworkTechnology, error) {
	return s.repo.FindAll()
}

// DeleteNetworkTechnology removes a network technology by ID
func (s *NetworkTechnologyService) DeleteNetworkTechnology(id string) error {
	if id == "" {
		return errors.New("network technology ID cannot be empty")
	}

	// Call repository to delete the entity by ID
	return s.repo.Delete(id)
}

// validateNetworkTechnology performs validation checks on a network technology entity
func (s *NetworkTechnologyService) validateNetworkTechnology(nt entities.NetworkTechnology) error {
	if nt.ID == "" {
		return errors.New("network technology ID cannot be empty")
	}
	if nt.Name == "" {
		return errors.New("network technology name cannot be empty")
	}
	if nt.Description == "" {
		return errors.New("network technology description cannot be empty")
	}
	return nil
}
