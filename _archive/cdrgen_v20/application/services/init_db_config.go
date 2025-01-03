package services

import (
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/domain/repositories"
	"log"
)

// BaselineService defines the service methods that interact with repositories.
type BaselineService struct {
	networkTechnologyRepo repositories.NetworkTechnologyRepository
	networkElementTypeRepo repositories.NetworkElementTypeRepository
	serviceTypeRepo        repositories.ServiceTypeRepository
}

// NewBaselineService creates a new instance of BaselineService.
func NewBaselineService(
	networkTechnologyRepo repositories.NetworkTechnologyRepository,
	networkElementTypeRepo repositories.NetworkElementTypeRepository,
	serviceTypeRepo repositories.ServiceTypeRepository,
) *BaselineService {
	return &BaselineService{
		networkTechnologyRepo: networkTechnologyRepo,
		networkElementTypeRepo: networkElementTypeRepo,
		serviceTypeRepo:        serviceTypeRepo,
	}
}

// InsertNetworkTechnology inserts a new network technology into the repository.
func (s *BaselineService) InsertNetworkTechnology(name, description string) error {
	networkTechnology := entities.NetworkTechnology{
		Name:        name,
		Description: description,
	}
	return s.networkTechnologyRepo.Insert(networkTechnology)
}

// GetAllNetworkTechnologies retrieves all network technologies.
func (s *BaselineService) GetAllNetworkTechnologies() ([]entities.NetworkTechnology, error) {
	return s.networkTechnologyRepo.GetAll()
}

// InsertNetworkElementType inserts a new network element type into the repository.
func (s *BaselineService) InsertNetworkElementType(name, description, networkTechnology string) error {
	networkElementType := entities.NetworkElementType{
		Name:             name,
		Description:      description,
		NetworkTechnology: networkTechnology,
	}
	return s.networkElementTypeRepo.Insert(networkElementType)
}

// GetAllNetworkElementTypes retrieves all network element types.
func (s *BaselineService) GetAllNetworkElementTypes() ([]entities.NetworkElementType, error) {
	return s.networkElementTypeRepo.GetAll()
}

// InsertServiceType inserts a new service type into the repository.
func (s *BaselineService) InsertServiceType(name, description, networkTechnology string) error {
	serviceType := entities.ServiceType{
		Name:             name,
		Description:      description,
		NetworkTechnology: networkTechnology,
	}
	return s.serviceTypeRepo.Insert(serviceType)
}

// GetAllServiceTypes retrieves all service types.
func (s *BaselineService) GetAllServiceTypes() ([]entities.ServiceType, error) {
	return s.serviceTypeRepo.GetAll()
}

