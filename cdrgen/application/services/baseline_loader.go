package services

import (
	"encoding/json"
	"fmt"
	"os"

	"github.com/mezni/wovoka/cdrgen/application/dtos"
	"github.com/mezni/wovoka/cdrgen/application/mappers"
	"github.com/mezni/wovoka/cdrgen/infrastructure/boltstore"
)

const (
	networkTechnologiesBucket = "network_technologies"
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
		return dtos.BaselineConfig{}, fmt.Errorf("error opening config file: %w", err)
	}
	defer file.Close()

	// Decode JSON into BaselineConfig struct
	var config dtos.BaselineConfig
	if err := json.NewDecoder(file).Decode(&config); err != nil {
		return dtos.BaselineConfig{}, fmt.Errorf("error decoding JSON: %w", err)
	}
	return config, nil
}

// LoadBaseline processes the baseline configuration.
func (ls *BaselineLoaderService) LoadBaseline() error {
	// Step 1: Load the configuration
	config, err := ls.LoadConfig()
	if err != nil {
		return fmt.Errorf("error loading configuration: %w", err)
	}

	// Step 2: Create a BaselineMapper instance
	mapper := &mappers.BaselineMapper{}

	// Step 3: Map DTOs to domain entities
	networkTechnologies, err := mapper.ToNetworkTechnologies(config.NetworkTechnologies)
	if err != nil {
		return fmt.Errorf("error mapping network technologies: %w", err)
	}

	// Step 4: Convert []entities.Location to []interface{} for saving in BoltDB
	networkTechnologiesAsInterfaces := make([]interface{}, len(networkTechnologies))
	for i, loc := range networkTechnologies {
		networkTechnologiesAsInterfaces[i] = loc
	}

	// Step 5: Save the data to BoltDB
	err = boltstore.SaveToBoltDB(ls.dbFile, networkTechnologiesBucket, networkTechnologiesAsInterfaces)
	if err != nil {
		return fmt.Errorf("error saving network technologies to DB: %w", err)
	}

	// Step 6: Print results for demonstration
	fmt.Printf("Mapped Network Technologies: %+v\n", networkTechnologies)
	fmt.Println("Baseline loaded successfully")
	return nil
}
