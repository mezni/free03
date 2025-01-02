package services

import (
	"github.com/mezni/wovoka/cdrgen/domain/entities"
	"github.com/mezni/wovoka/cdrgen/infrastructure/sqlitestore"
	"encoding/json"
	"fmt"
	"io/ioutil"
)

// ConfigLoaderService handles the loading and saving of data.
type ConfigLoaderService struct {
	NetworkTechnologyRepo sqlitestore.NetworkTechnologyRepository
}

// NewConfigLoaderService creates a new instance of ConfigLoaderService.
func NewConfigLoaderService(networkTechnologyRepo sqlitestore.NetworkTechnologyRepository) *ConfigLoaderService {
	return &ConfigLoaderService{
		NetworkTechnologyRepo: networkTechnologyRepo,
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

	return nil
}
