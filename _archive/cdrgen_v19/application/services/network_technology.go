package services

import (
	"encoding/json"
	"fmt"
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"io/ioutil"
)

// ConfigLoaderService handles the loading and saving of data.
type ConfigLoaderService struct {
	NetworkTechnologyRepo sqlitestore.NetworkTechnologyRepository
	NetworkElementRepo    sqlitestore.NetworkElementRepository
	ServiceTypeRepo       sqlitestore.ServiceTypeRepository
}

// NewConfigLoaderService creates a new instance of ConfigLoaderService.
func NewConfigLoaderService(
	networkTechnologyRepo sqlitestore.NetworkTechnologyRepository,
	networkElementRepo sqlitestore.NetworkElementRepository,
	serviceTypeRepo sqlitestore.ServiceTypeRepository) *ConfigLoaderService {

	return &ConfigLoaderService{
		NetworkTechnologyRepo: networkTechnologyRepo,
		NetworkElementRepo:    networkElementRepo,
		ServiceTypeRepo:       serviceTypeRepo,
	}
}

// LoadAndSaveData loads data from a JSON file and saves it to the database.
func (app *ConfigLoaderService) LoadAndSaveData(filename string) error {
	// Read the file content
	data, err := ioutil.ReadFile(filename)
	if err != nil {
		return fmt.Errorf("could not read file: %v", err)
	}

	// Unmarshal JSON data
	var jsonData struct {
		NetworkTechnologies []entities.NetworkTechnology `json:"network_technologies"`
		NetworkElements     []entities.NetworkElement    `json:"network_element_types"`
		ServiceTypes        []entities.ServiceType       `json:"service_types"`
	}
	if err := json.Unmarshal(data, &jsonData); err != nil {
		return fmt.Errorf("could not unmarshal json: %v", err)
	}

	// Save network technologies to the database
	for _, nt := range jsonData.NetworkTechnologies {
		if err := app.NetworkTechnologyRepo.Save(nt); err != nil {
			return fmt.Errorf("error saving network technology: %v", err)
		}
	}

	// Save network elements to the database
	for _, ne := range jsonData.NetworkElements {
		if err := app.NetworkElementRepo.Save(ne); err != nil {
			return fmt.Errorf("error saving network element: %v", err)
		}
	}

	// Save service types to the database
	for _, st := range jsonData.ServiceTypes {
		if err := app.ServiceTypeRepo.Save(st); err != nil {
			return fmt.Errorf("error saving service type: %v", err)
		}
	}

	return nil
}
