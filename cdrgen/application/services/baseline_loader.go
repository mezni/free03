package services

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
)

type BaselineLoaderService struct {
	configFile string
	dbFile     string
}

func NewBaselineLoaderService(configFile, dbFile string) *BaselineLoaderService {
	return &BaselineLoaderService{
		configFile: configFile,
		dbFile:     dbFile,
	}
}

// LoadConfig loads the baseline configuration from the JSON file.
func (ls *BaselineLoaderService) LoadConfig() (dtos.BaselineConfig, error) {
	// Open the JSON config file
	file, err := os.Open(ls.configFile)
	if err != nil {
		return dtos.BaselineConfig{}, fmt.Errorf("error opening file: %v", err)
	}
	defer file.Close()

	// Decode JSON into BaselineConfig struct
	var config dtos.BaselineConfig
	if err := json.NewDecoder(file).Decode(&config); err != nil {
		return dtos.BaselineConfig{}, fmt.Errorf("error decoding JSON: %v", err)
	}
	return config, nil
}

// LoadBaseline processes the baseline configuration.
func (ls *BaselineLoaderService) LoadBaseline() error {
	// Load the configuration
	config, err := ls.LoadConfig()
	if err != nil {
		return fmt.Errorf("error loading config: %v", err)
	}

	// Create a BaselineMapper instance
	mapper := &mappers.BaselineMapper{}

	// Map DTOs to domain entities
	networkTechnologies, err := mapper.ToNetworkTechnologies(config.NetworkTechnologies)
	if err != nil {
		return fmt.Errorf("error mapping network technologies: %v", err)
	}

	// Print the mapped configuration for demonstration
	fmt.Printf("Mapped Network Technologies: %+v\n", networkTechnologies)

	fmt.Println("Baseline loaded successfully")
	return nil
}
