package services

import (
	"encoding/json"
	"fmt"
	"github.com/mezni/wovoka/domain/entities"
	"github.com/mezni/wovoka/domain/interfaces"
	"os"
)

// ServiceService handles the business logic for services and interacts with the repository.
type ServiceService struct {
	repo interfaces.ServiceRepository
}

// NewServiceService returns a new instance of ServiceService with the injected repository.
func NewServiceService(repo interfaces.ServiceRepository) *ServiceService {
	return &ServiceService{repo: repo}
}

// LoadServicesFromFile loads services from a JSON file into a slice of entities.Service.
func (ss *ServiceService) LoadServicesFromFile(filePath string) ([]entities.Service, error) {
	// Open the services.json file
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("could not open services file: %v", err)
	}
	defer file.Close()

	// Decode the JSON data into a slice of services
	var services []entities.Service
	decoder := json.NewDecoder(file)
	if err := decoder.Decode(&services); err != nil {
		return nil, fmt.Errorf("could not decode services data: %v", err)
	}

	// Return the loaded services
	return services, nil
}

// LoadAndStoreServices loads services from a configuration file and stores them in the repository.
func (ss *ServiceService) LoadAndStoreServices(filePath string) error {
	services, err := ss.LoadServicesFromFile(filePath)
	if err != nil {
		return err
	}

	// Store each service in the repository
	for _, service := range services {
		if err := ss.repo.Create(&service); err != nil {
			return err
		}
	}

	return nil
}

// ListServices retrieves all services stored in the repository.
func (ss *ServiceService) ListServices() ([]*entities.Service, error) {
	return ss.repo.List()
}
